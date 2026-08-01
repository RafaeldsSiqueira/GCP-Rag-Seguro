from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class IngestRequest(BaseModel):
    documento_id: str = Field(..., json_schema_extra={"example": "hero-001"})
    titulo: str = Field(..., json_schema_extra={"example": "Ficha Batman"})
    conteudo_bruto: str = Field(..., json_schema_extra={"example": "Bruce Wayne mora em Gotham City e sua base secreta e a Batcaverna."})

class IngestResponse(BaseModel):
    status: str = "SUCCESS"
    documento_id: str
    conteudo_sanitizado: str
    vetor_dimensao: int = 768
    mensagens: str = "Documento sanitizado via DLP e armazenado no Firestore Vector Search."

class QueryRequest(BaseModel):
    pergunta: str = Field(..., json_schema_extra={"example": "Onde fica a base do Batman?"})
    top_k: int = Field(default=3, ge=1, le=10)

class QueryResponse(BaseModel):
    status: str = "success"
    pergunta: str
    resposta_gerada: str
    documentos_relacionados: List[Dict[str, Any]]
