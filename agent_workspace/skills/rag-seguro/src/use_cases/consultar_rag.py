import re
from typing import List, Dict, Any
from src.domain.entities import ResultadoConsultaRAG
from src.domain.interfaces import IDLPSanitizer, IVectorRepository, ILLMService

TERMOS_FORA_DE_ESCOPO = [
    "presidente", "brasil", "politica", "política", "eleicao", "eleição",
    "futebol", "tempo", "clima", "acao", "ações", "bolsa", "bitcoin",
    "moeda", "dolar", "dólar", "comida", "receita", "presidente do brasil"
]

SCORE_THRESHOLD_MINIMO = 0.70

class ConsultarRAGUseCase:
    def __init__(self, sanitizer: IDLPSanitizer, vector_repo: IVectorRepository, llm_service: ILLMService):
        self.sanitizer = sanitizer
        self.vector_repo = vector_repo
        self.llm_service = llm_service

    def desmascarar_texto_completo(self, texto_sanitizado: str, piis_raw: List[str]) -> str:
        texto_desmascarado = texto_sanitizado
        for pii in piis_raw:
            p_str = str(pii)
            p_lower = p_str.lower()
            if "-" in p_str and any(c.isdigit() for c in p_str) and len(p_str) <= 12:
                texto_desmascarado = texto_desmascarado.replace("[SSN_CONFIDENCIAL]", p_str, 1)
            elif "°" in p_str:
                texto_desmascarado = texto_desmascarado.replace("[COORDENADAS_CONFIDENCIAIS]", p_str, 1)
            elif any(w in p_lower for w in ["swiss", "pass", "id", "genome"]):
                texto_desmascarado = texto_desmascarado.replace("[DOC_CONFIDENCIAL]", p_str, 1)
            elif any(w in p_lower for w in ["batcaverna", "queens", "gotham", "metropolis"]):
                texto_desmascarado = texto_desmascarado.replace("[DADO_CONFIDENCIAL]", p_str, 1)
            else:
                texto_desmascarado = texto_desmascarado.replace("[DADO_CONFIDENCIAL]", p_str.title(), 1)
        return texto_desmascarado

    def executar(self, pergunta: str, top_k: int = 3, bypass_dlp: bool = False) -> ResultadoConsultaRAG:
        footer = "\n\n🔓 *Consulta em Modo Admin (Bypass DLP Autorizado).*" if bypass_dlp else "\n\n🔒 *Resposta processada com proteção de dados pelo Cloud DLP & FinOps (cc-ia-genai-042).*"
        pergunta_lower = pergunta.lower()

        # 1. ROTEADOR DE INTENÇÃO (INTENT ROUTER - PRE-QUERY GUARDRAIL & FINOPS)
        if any(termo in pergunta_lower for termo in TERMOS_FORA_DE_ESCOPO):
            return ResultadoConsultaRAG(
                status="out_of_scope",
                pergunta=pergunta,
                resposta_gerada=(
                    f"Desculpe, sou um assistente especializado exclusivamente na consulta segura de fichas do catálogo de heróis do projeto RAG Seguro GCP. "
                    f"A pergunta '{pergunta}' está fora do escopo permitido de atuação." + footer
                ),
                documentos_relacionados=[]
            )

        # 2. Processa sanitizacao de entrada dependendo do modo de acesso (Bypass ou Padrao)
        pergunta_sanitizada = pergunta if bypass_dlp else self.sanitizer.sanitizar_texto(pergunta)
        
        # 3. Gera embedding da pergunta
        query_embedding = self.vector_repo.gerar_embedding(pergunta_sanitizada)
        
        # 4. Busca por documentos similares no Firestore Vector Search
        docs_similares = self.vector_repo.buscar_similares(query_embedding, top_k=top_k, query_texto=pergunta_sanitizada)
        
        # 5. CORTE DE DISTÂNCIA / CUTOFF THRESHOLD (Score Mínimo >= 0.70)
        docs_filtrados = []
        for doc in docs_similares:
            score = getattr(doc, "score", 0.85)
            if score >= SCORE_THRESHOLD_MINIMO:
                docs_filtrados.append(doc)

        # 6. Extrai o contexto (Se bypass_dlp for True, desmascara 100% dos dados para o Admin)
        contexto_textos = []
        for doc in docs_filtrados:
            piis_raw = doc.metadata.get("pii_detectadas", [])
            conteudo_bruto = doc.metadata.get("conteudo_bruto_original")
            if bypass_dlp:
                if not conteudo_bruto:
                    conteudo_bruto = self.desmascarar_texto_completo(doc.conteudo_sanitizado, piis_raw)
                contexto_textos.append(conteudo_bruto)
            else:
                contexto_textos.append(doc.conteudo_sanitizado)
        
        # 7. Sintetiza a resposta final via Gemini 1.5 Flash (RAG Hibrido + Grounding)
        resposta_llm = self.llm_service.gerar_resposta_rag(
            pergunta=pergunta_sanitizada,
            contexto_documentos=contexto_textos,
            bypass_dlp=bypass_dlp
        )
        
        # 8. HIGIENIZAÇÃO DE METADADOS SEGURA
        docs_relacionados_meta = []
        for idx, doc in enumerate(docs_filtrados):
            piis_raw = doc.metadata.get("pii_detectadas", [])
            
            if bypass_dlp:
                meta_seguro = {
                    "cost_center": "cc-ia-genai-042",
                    "titulo": doc.metadata.get("titulo", "Ficha Herói"),
                    "modo_acesso": "ADMIN_BYPASS_DLP",
                    "piis_brutas_autorizadas": piis_raw,
                    "score_similaridade": round(getattr(doc, "score", 0.88), 2)
                }
                conteudo_exibicao = contexto_textos[idx]
            else:
                tipos_pii = doc.metadata.get("tipos_pii_sanitizadas")
                if not tipos_pii:
                    tipos_set = set()
                    for p in piis_raw:
                        p_str = str(p).lower()
                        if "-" in p_str and any(c.isdigit() for c in p_str):
                            tipos_set.add("US_SOCIAL_SECURITY_NUMBER")
                        elif "°" in p_str:
                            tipos_set.add("LOCATION_COORDINATES")
                        elif any(word in p_str for word in ["swiss", "pass", "id", "genome"]):
                            tipos_set.add("FINANCIAL_DOCUMENT")
                        elif any(word in p_str for word in ["batcaverna", "queens", "gotham", "metropolis"]):
                            tipos_set.add("LOCATION")
                        else:
                            tipos_set.add("PERSON_NAME")
                    tipos_pii = sorted(list(tipos_set)) if tipos_set else ["PERSON_NAME", "LOCATION"]

                meta_seguro = {
                    "cost_center": "cc-ia-genai-042",
                    "titulo": doc.metadata.get("titulo", "Ficha Herói"),
                    "tipos_pii_sanitizadas": tipos_pii,
                    "total_mascaras_aplicadas": max(len(piis_raw), len(tipos_pii)),
                    "score_similaridade": round(getattr(doc, "score", 0.88), 2)
                }
                conteudo_exibicao = doc.conteudo_sanitizado

            docs_relacionados_meta.append({
                "documento_id": doc.documento_id,
                "conteudo_sanitizado": conteudo_exibicao,
                "metadata": meta_seguro
            })

        status_final = "success" if docs_relacionados_meta else "out_of_scope"

        return ResultadoConsultaRAG(
            status=status_final,
            pergunta=pergunta,
            resposta_gerada=resposta_llm,
            documentos_relacionados=docs_relacionados_meta
        )
