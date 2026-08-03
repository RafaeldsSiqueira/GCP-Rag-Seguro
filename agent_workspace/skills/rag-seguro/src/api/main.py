import os
import logging
from typing import Optional
from fastapi import FastAPI, HTTPException, Security, status, Depends, Request
from fastapi.security import APIKeyHeader
from src.api.schemas import IngestRequest, IngestResponse, QueryRequest, QueryResponse
from src.domain.entities import DocumentoBruto
from src.infrastructure.dlp_sanitizer import CloudDLPSanitizer
from src.infrastructure.firestore_vector_repo import FirestoreVectorRepository
from src.infrastructure.gemini_client import GeminiFlashLLMService
from src.use_cases.ingestar_documento import IngestarDocumentoUseCase
from src.use_cases.consultar_rag import ConsultarRAGUseCase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("rag_seguro_api")

app = FastAPI(
    title="RAG Seguro GCP API",
    description="API Serverless de Busca Semântica com Sanitização de PII via Cloud DLP, Gemini 1.5 Flash, Autenticação X-API-Key e Suporte a Bypass Privilegiado X-DLP-Bypass-Key",
    version="1.0.0"
)

# Segurança: NÃO deixar defaults de chaves no código.
# APP_API_KEY e APP_BYPASS_KEY devem ser provisionadas via Secret Manager ou variáveis de ambiente no runtime.
# Se for necessário testar a API manualmente, gere uma nova chave temporária e injete-a via Secret Manager ou export APP_API_KEY="sua_chave_temp".
EXPECTED_API_KEY = os.environ.get("APP_API_KEY")
EXPECTED_BYPASS_KEY = os.environ.get("APP_BYPASS_KEY")

# Falha rápida na inicialização para evitar rodar com um valor padrão inseguro
if not EXPECTED_API_KEY:
    raise RuntimeError(
        "APP_API_KEY não definido. Configure via Secret Manager (recomendado) ou variável de ambiente antes de iniciar o serviço."
    )

PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "rag-seguro-gcp")

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def verificar_api_key(api_key: str = Depends(api_key_header)):
    if not api_key or api_key != EXPECTED_API_KEY:
        logger.warning("Tentativa de acesso negada: X-API-Key invalida ou ausente.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Acesso Negado: Cabecalho 'X-API-Key' invalido ou ausente."
        )
    return api_key

# Conexao com os servicos reais da GCP se disponiveis, senao usa fallback
firestore_client = None
try:
    from google.cloud import firestore
    firestore_client = firestore.Client(project=PROJECT_ID)
    logger.info("✅ Firestore Native Client conectado com sucesso.")
except Exception as e:
    logger.warning(f"⚠️ Usando fallback em memória para o Firestore: {e}")

dlp_client = None
try:
    import google.cloud.dlp_v2 as dlp
    dlp_client = dlp.DlpServiceClient()
    logger.info("✅ Cloud DLP Service Client conectado com sucesso.")
except Exception as e:
    logger.warning(f"⚠️ Usando fallback local para o Cloud DLP: {e}")

gemini_model = None
try:
    import google.generativeai as genai
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    if gemini_api_key:
        genai.configure(api_key=gemini_api_key)
        for model_candidate in ["gemini-1.5-flash-latest", "gemini-1.5-flash", "gemini-2.0-flash", "gemini-1.5-pro"]:
            try:
                gemini_model = genai.GenerativeModel(model_candidate)
                logger.info(f"✅ Gemini Client conectado com sucesso utilizando o modelo '{model_candidate}'.")
                break
            except Exception as ex_m:
                logger.warning(f"Candidato {model_candidate} nao suportado: {ex_m}")
except Exception as e:
    logger.warning(f"⚠️ Usando fallback local para o Gemini: {e}")

# Inicializacao dos adaptadores com os clientes reais da GCP
sanitizer = CloudDLPSanitizer(dlp_client_adapter=dlp_client, project_id=PROJECT_ID)
vector_repo = FirestoreVectorRepository(firestore_db=firestore_client, project_id=PROJECT_ID)
llm_service = GeminiFlashLLMService(gemini_client=gemini_model)

ingestar_use_case = IngestarDocumentoUseCase(sanitizer=sanitizer, vector_repo=vector_repo)
consultar_use_case = ConsultarRAGUseCase(sanitizer=sanitizer, vector_repo=vector_repo, llm_service=llm_service)

@app.get("/healthz", status_code=status.HTTP_200_OK)
def health_check():
    return {
        "status": "HEALTHY",
        "service": "rag-seguro-gcp",
        "cost_center": "cc-ia-genai-042",
        "firestore_connected": firestore_client is not None,
        "dlp_connected": dlp_client is not None,
        "gemini_connected": gemini_model is not None,
        "auth_required": "X-API-Key",
        "dlp_bypass_supported": "X-DLP-Bypass-Key"
    }

@app.post("/api/v1/ingest", response_model=IngestResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(verificar_api_key)])
def ingest_documento(request: IngestRequest):
    try:
        doc_bruto = DocumentoBruto(
            documento_id=request.documento_id,
            titulo=request.titulo,
            conteudo_bruto=request.conteudo_bruto
        )
        vetor_doc = ingestar_use_case.executar(doc_bruto)
        
        return IngestResponse(
            status="SUCCESS",
            documento_id=vetor_doc.documento_id,
            conteudo_sanitizado=vetor_doc.conteudo_sanitizado,
            vetor_dimensao=len(vetor_doc.embedding)
        )
    except Exception as e:
        logger.error(f"Erro no processamento de ingestao: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Falha ao sanitizar e ingestar documento: {str(e)}"
        )

@app.post("/api/v1/query", response_model=QueryResponse, status_code=status.HTTP_200_OK, dependencies=[Depends(verificar_api_key)])
def query_rag(request_body: QueryRequest, http_request: Request):
    try:
        bypass_header = http_request.headers.get("X-DLP-Bypass-Key") or http_request.headers.get("x-dlp-bypass-key")
        bypass_dlp = bool(bypass_header and bypass_header == EXPECTED_BYPASS_KEY)
        if bypass_dlp:
            logger.info("🔓 Acesso privilegiado ativado via X-DLP-Bypass-Key.")
            
        resultado = consultar_use_case.executar(pergunta=request_body.pergunta, top_k=request_body.top_k, bypass_dlp=bypass_dlp)
        return QueryResponse(
            status=resultado.status,
            pergunta=resultado.pergunta,
            resposta_gerada=resultado.resposta_gerada,
            documentos_relacionados=resultado.documentos_relacionados
        )
    except Exception as e:
        logger.error(f"Erro no processamento da consulta RAG: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Falha na consulta RAG: {str(e)}"
        )
