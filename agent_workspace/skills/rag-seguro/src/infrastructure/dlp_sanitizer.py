import logging
from typing import List
from src.domain.entities import DocumentoBruto, DocumentoSanitizado
from src.domain.interfaces import IDLPSanitizer
from src.domain.rules import LocalPIIRules

logger = logging.getLogger(__name__)

class CloudDLPSanitizer(IDLPSanitizer):
    def __init__(self, dlp_client_adapter=None, project_id: str = "poc-rag-seguro-gcp-042"):
        self.dlp_client = dlp_client_adapter
        self.project_id = project_id
        self.cost_center = "cc-ia-genai-042"

    def sanitizar(self, documento: DocumentoBruto) -> DocumentoSanitizado:
        try:
            if self.dlp_client and hasattr(self.dlp_client, "sanitizar"):
                return self.dlp_client.sanitizar(documento)
            
            # Fallback deterministico com regras locais (DLP Local/Sandbox)
            texto_sanitizado, piis = LocalPIIRules.sanitizar_localmente(documento.conteudo_bruto)
            return DocumentoSanitizado(
                documento_id=documento.documento_id,
                titulo=documento.titulo,
                conteudo_sanitizado=texto_sanitizado,
                pii_detectadas=piis,
                cost_center=self.cost_center
            )
        except Exception as e:
            logger.error(f"Erro na sanitizacao DLP para o documento {documento.documento_id}: {e}")
            texto_sanitizado, piis = LocalPIIRules.sanitizar_localmente(documento.conteudo_bruto)
            return DocumentoSanitizado(
                documento_id=documento.documento_id,
                titulo=documento.titulo,
                conteudo_sanitizado=texto_sanitizado,
                pii_detectadas=piis,
                cost_center=self.cost_center
            )

    def sanitizar_texto(self, texto: str) -> str:
        if self.dlp_client and hasattr(self.dlp_client, "sanitizar_texto"):
            return self.dlp_client.sanitizar_texto(texto)
        texto_sanitizado, _ = LocalPIIRules.sanitizar_localmente(texto)
        return texto_sanitizado

    def sanitizar_lote(self, textos: List[str]) -> List[str]:
        return [self.sanitizar_texto(t) for t in textos]
