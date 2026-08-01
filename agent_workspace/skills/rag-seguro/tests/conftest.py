import pytest
import os
import json
from typing import List, Dict
from src.domain.entities import DocumentoBruto, DocumentoSanitizado, VetorDocumento
from src.domain.interfaces import IDLPSanitizer, IVectorRepository, ILLMService
from src.domain.rules import LocalPIIRules

class FakeDLPSanitizer(IDLPSanitizer):
    def sanitizar(self, doc: DocumentoBruto) -> DocumentoSanitizado:
        texto_sanitizado, piis = LocalPIIRules.sanitizar_localmente(doc.conteudo_bruto)
        return DocumentoSanitizado(
            documento_id=doc.documento_id,
            titulo=doc.titulo,
            conteudo_sanitizado=texto_sanitizado,
            pii_detectadas=piis
        )

    def sanitizar_texto(self, texto: str) -> str:
        texto_sanitizado, _ = LocalPIIRules.sanitizar_localmente(texto)
        return texto_sanitizado

class FakeFirestoreVectorRepository(IVectorRepository):
    def __init__(self):
        self.store: Dict[str, VetorDocumento] = {}

    def gerar_embedding(self, texto: str) -> List[float]:
        return [0.1] * 768

    def salvar_vetor(self, vetor_doc: VetorDocumento) -> bool:
        self.store[vetor_doc.documento_id] = vetor_doc
        return True

    def buscar_similares(self, query_embedding: List[float], top_k: int = 3, **kwargs) -> List[VetorDocumento]:
        return list(self.store.values())[:top_k]

class FakeGeminiLLMService(ILLMService):
    def gerar_resposta_rag(self, pergunta: str, contexto_documentos: List[str], bypass_dlp: bool = False) -> str:
        footer = "\n\n🔓 *Consulta em Modo Admin (Bypass DLP Autorizado).*" if bypass_dlp else "\n\n🔒 *Resposta processada com proteção de dados pelo Cloud DLP & FinOps (cc-ia-genai-042).*"
        return f"Resposta sintetizada pelo modelo gemini-1.5-flash com base em {len(contexto_documentos)} contexto(s)." + footer

@pytest.fixture
def fake_dlp():
    return FakeDLPSanitizer()

@pytest.fixture
def fake_vector_repo():
    return FakeFirestoreVectorRepository()

@pytest.fixture
def fake_gemini():
    return FakeGeminiLLMService()

@pytest.fixture
def dataset_mock_herois():
    caminho = "/home/rafael/Documentos/rag-seguro-gcp/.sandbox/hero_dataset_mock.json"
    if not os.path.exists(caminho):
        caminho = "/home/rafael/Documentos/rag-seguro-gcp/agent_workspace/harness/datasets/hero_dataset_mock.json"
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)
