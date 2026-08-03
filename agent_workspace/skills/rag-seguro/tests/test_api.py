import os
os.environ.setdefault("APP_API_KEY", "test-key")
os.environ.setdefault("APP_BYPASS_KEY", "test-bypass")

from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)
AUTH_HEADERS = {"X-API-Key": os.environ["APP_API_KEY"]}
ADMIN_HEADERS = {"X-API-Key": os.environ["APP_API_KEY"], "X-DLP-Bypass-Key": os.environ["APP_BYPASS_KEY"]}


def test_api_acesso_negado_sem_chave():
    payload = {
        "documento_id": "hero-001",
        "titulo": "Ficha Batman",
        "conteudo_bruto": "Bruce Wayne mora em Gotham City"
    }
    response = client.post("/api/v1/ingest", json=payload)
    assert response.status_code == 401
    assert "Acesso Negado" in response.json()["detail"]


def test_api_ingest_documento_autenticado():
    payload = {
        "documento_id": "hero-001",
        "titulo": "Ficha Batman",
        "conteudo_bruto": "Bruce Wayne mora em Gotham City e sua base e a Batcaverna"
    }
    
    response = client.post("/api/v1/ingest", json=payload, headers=AUTH_HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "SUCCESS"
    assert data["documento_id"] == "hero-001"
    assert "[DADO_CONFIDENCIAL]" in data["conteudo_sanitizado"]
    assert data["vetor_dimensao"] == 768


def test_api_query_rag_autenticado():
    client.post("/api/v1/ingest", json={
        "documento_id": "spidey-01",
        "titulo": "Ficha Homem-Aranha",
        "conteudo_bruto": "Peter Parker mora no Queens"
    }, headers=AUTH_HEADERS)
    
    query_payload = {
        "pergunta": "Onde mora o Peter Parker?",
        "top_k": 3
    }
    
    response = client.post("/api/v1/query", json=query_payload, headers=AUTH_HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["pergunta"] == "Onde mora o Peter Parker?"
    assert "gemini-1.5-flash" in data["resposta_gerada"].lower()
    assert len(data["documentos_relacionados"]) >= 1
    
    # Valida que metadados NAO vazam PIIs brutas
    meta = data["documentos_relacionados"][0]["metadata"]
    assert "tipos_pii_sanitizadas" in meta
    assert isinstance(meta["tipos_pii_sanitizadas"], list)
    assert "bruce wayne" not in str(meta).lower()


def test_api_query_fora_do_escopo_guardrail():
    query_payload = {
        "pergunta": "Quem e o presidente do Brasil?",
        "top_k": 1
    }
    
    response = client.post("/api/v1/query", json=query_payload, headers=AUTH_HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "out_of_scope"
    assert "fora do escopo" in data["resposta_gerada"].lower()
    assert len(data["documentos_relacionados"]) == 0


def test_api_query_rag_admin_bypass_dlp():
    client.post("/api/v1/ingest", json={
        "documento_id": "batman-admin",
        "titulo": "Ficha Batman Admin",
        "conteudo_bruto": "Bruce Wayne mora em Gotham City e sua base e a Batcaverna"
    }, headers=AUTH_HEADERS)
    
    query_payload = {
        "pergunta": "Onde fica a base do Batman?",
        "top_k": 1
    }
    
    response = client.post("/api/v1/query", json=query_payload, headers=ADMIN_HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "Bypass DLP Autorizado" in data["resposta_gerada"]
    
    meta = data["documentos_relacionados"][0]["metadata"]
    assert meta["modo_acesso"] == "ADMIN_BYPASS_DLP"
    assert "piis_brutas_autorizadas" in meta
