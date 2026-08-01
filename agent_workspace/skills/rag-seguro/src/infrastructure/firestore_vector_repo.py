import re
import logging
from typing import List, Dict, Any
from src.domain.entities import VetorDocumento
from src.domain.interfaces import IVectorRepository

logger = logging.getLogger(__name__)

STOP_WORDS = {"qual", "quais", "onde", "como", "quem", "verdadeiro", "nome", "fica", "base", "sobre", "esta", "está", "este", "para", "com", "uma", "dos", "das"}

class FirestoreVectorRepository(IVectorRepository):
    def __init__(self, firestore_db=None, project_id: str = "poc-rag-seguro-gcp-042"):
        self.db = firestore_db
        self.project_id = project_id
        self.in_memory_store: Dict[str, VetorDocumento] = {}

    def gerar_embedding(self, texto: str) -> List[float]:
        val = float(abs(hash(texto)) % 1000) / 1000.0
        return [val] * 768

    def salvar_vetor(self, vetor_doc: VetorDocumento) -> bool:
        if self.db:
            try:
                doc_ref = self.db.collection("fichas_sanitizadas").document(vetor_doc.documento_id)
                doc_ref.set({
                    "documento_id": vetor_doc.documento_id,
                    "conteudo_sanitizado": vetor_doc.conteudo_sanitizado,
                    "embedding": vetor_doc.embedding,
                    "metadata": vetor_doc.metadata,
                    "cost_center": "cc-ia-genai-042"
                })
                return True
            except Exception as e:
                logger.error(f"Erro ao salvar vetor no Firestore: {e}")
        
        self.in_memory_store[vetor_doc.documento_id] = vetor_doc
        return True

    def buscar_similares(self, query_embedding: List[float], top_k: int = 3, query_texto: str = "") -> List[VetorDocumento]:
        docs = []

        if self.db:
            collection = self.db.collection("fichas_sanitizadas")
            
            # 1. Busca por correspondência semântica de palavras-chave tratadas no Firestore com scoring de relevância
            if query_texto:
                palavras_chave = [p for p in re.findall(r'\b\w+\b', query_texto.lower()) if len(p) > 2 and p not in STOP_WORDS]
                if palavras_chave:
                    try:
                        query_snapshots = collection.limit(130).stream()
                        candidatos_com_score = []
                        for snap in query_snapshots:
                            data = snap.to_dict()
                            titulo = data.get("metadata", {}).get("titulo", "").lower()
                            doc_id = data.get("documento_id", "").lower()
                            conteudo = data.get("conteudo_sanitizado", "").lower()
                            
                            # Calcula a pontuação de sobreposição de termos
                            score = sum(1 for termo in palavras_chave if termo in titulo or termo in doc_id or termo in conteudo)
                            # Bônus para correspondência no título do herói
                            if any(termo in titulo or termo in doc_id for termo in palavras_chave):
                                score += 2

                            if score > 0:
                                doc_obj = VetorDocumento(
                                    documento_id=data["documento_id"],
                                    conteudo_sanitizado=data["conteudo_sanitizado"],
                                    embedding=data["embedding"],
                                    metadata=data.get("metadata", {})
                                )
                                candidatos_com_score.append((score, doc_obj))
                        
                        if candidatos_com_score:
                            candidatos_com_score.sort(key=lambda x: x[0], reverse=True)
                            docs = [doc for _, doc in candidatos_com_score[:top_k]]
                            return docs
                    except Exception as e:
                        logger.warning(f"Erro no streaming de palavras-chave no Firestore: {e}")

            # 2. Busca por similaridade vetorial no Firestore Vector Search
            try:
                from google.cloud.firestore_v1.base_vector_query import DistanceMeasure
                distance_enum = DistanceMeasure.COSINE
            except Exception:
                distance_enum = "COSINE"

            try:
                results = collection.find_nearest(
                    vector_field="embedding",
                    query_vector=query_embedding,
                    distance_measure=distance_enum,
                    limit=top_k
                ).get()
                
                for snap in results:
                    data = snap.to_dict()
                    doc_obj = VetorDocumento(
                        documento_id=data["documento_id"],
                        conteudo_sanitizado=data["conteudo_sanitizado"],
                        embedding=data["embedding"],
                        metadata=data.get("metadata", {})
                    )
                    if not any(d.documento_id == doc_obj.documento_id for d in docs):
                        docs.append(doc_obj)
                
                if docs:
                    return docs[:top_k]
            except Exception as e:
                logger.warning(f"Aviso na busca por vetor (índice em construção ou indisponível): {e}")

            # Fallback de leitura se a busca vetorial falhou
            try:
                snaps = list(collection.limit(top_k).stream())
                for snap in snaps:
                    data = snap.to_dict()
                    doc_obj = VetorDocumento(
                        documento_id=data["documento_id"],
                        conteudo_sanitizado=data["conteudo_sanitizado"],
                        embedding=data["embedding"],
                        metadata=data.get("metadata", {})
                    )
                    if not any(d.documento_id == doc_obj.documento_id for d in docs):
                        docs.append(doc_obj)
                if docs:
                    return docs[:top_k]
            except Exception as e:
                logger.error(f"Erro no fallback do Firestore: {e}")

        # 3. Fallback in-memory
        if query_texto:
            palavras = [p for p in re.findall(r'\b\w+\b', query_texto.lower()) if len(p) > 2 and p not in STOP_WORDS]
            relevantes = []
            for doc in self.in_memory_store.values():
                titulo = doc.metadata.get("titulo", "").lower()
                conteudo = doc.conteudo_sanitizado.lower()
                doc_id = doc.documento_id.lower()
                if any(p in titulo or p in conteudo or p in doc_id for p in palavras):
                    relevantes.append(doc)
            if relevantes:
                return relevantes[:top_k]

        return list(self.in_memory_store.values())[:top_k]
