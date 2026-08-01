from abc import ABC, abstractmethod
from typing import List
from src.domain.entities import DocumentoBruto, DocumentoSanitizado, VetorDocumento

class IDLPSanitizer(ABC):
    @abstractmethod
    def sanitizar(self, doc: DocumentoBruto) -> DocumentoSanitizado:
        pass

    @abstractmethod
    def sanitizar_texto(self, texto: str) -> str:
        pass

class IVectorRepository(ABC):
    @abstractmethod
    def gerar_embedding(self, texto: str) -> List[float]:
        pass

    @abstractmethod
    def salvar_vetor(self, vetor_doc: VetorDocumento) -> bool:
        pass

    @abstractmethod
    def buscar_similares(self, query_embedding: List[float], top_k: int = 3, **kwargs) -> List[VetorDocumento]:
        pass

class ILLMService(ABC):
    @abstractmethod
    def gerar_resposta_rag(self, pergunta: str, contexto_documentos: List[str], bypass_dlp: bool = False) -> str:
        pass
