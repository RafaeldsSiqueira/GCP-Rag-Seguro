import os
import logging
from typing import List
from src.domain.entities import DocumentoBruto, DocumentoSanitizado
from src.domain.interfaces import IDLPSanitizer
from src.domain.rules import LocalPIIRules

logger = logging.getLogger(__name__)

# SECURITY NOTE:
# Não armazene valores reais de projeto ou secrets no código-fonte.
# Configure GCP_PROJECT_ID e os clients via variáveis de ambiente ou injeção de dependência.
# Para testes da API: gere uma nova chave temporária e injete-a via Secret Manager ou variável de ambiente:
# export APP_API_KEY="sua_chave_temporaria"

DEFAULT_PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
if not DEFAULT_PROJECT_ID:
    logger.warning(
        "GCP_PROJECT_ID não definido — utilizando valor padrão para ambiente local. Em produção, configure GCP_PROJECT_ID via env/Secret Manager."
    )

class CloudDLPSanitizer(IDLPSanitizer):
    def __init__(self, dlp_client_adapter=None, project_id: str = None):
        # Preferir passar explicitamente o client e project_id em runtime (injeção via Secret Manager / env vars).
        self.dlp_client = dlp_client_adapter
        # Use project_id passado, ou o GCP_PROJECT_ID da env, ou um identificador local padrão
        self.project_id = project_id or DEFAULT_PROJECT_ID or "poc-rag-seguro-gcp-042"
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
