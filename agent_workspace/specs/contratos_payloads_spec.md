# 📑 Especificação de Contratos de Payload & APIs

Esta especificação define os contratos de dados para injeção de documentos e consulta RAG.

---

## 1. Endpoint: `POST /api/v1/ingest`

### Payload de Entrada:
```json
{
  "documento_id": "hero-001",
  "titulo": "Ficha Batman",
  "conteudo_bruto": "Bruce Wayne mora em Gotham City e sua base secreta é a Batcaverna."
}
```

### Resposta esperada (HTTP 200):
```json
{
  "status": "SUCCESS",
  "documento_id": "hero-001",
  "conteudo_sanitizado": "[DADO_CONFIDENCIAL] mora em [DADO_CONFIDENCIAL] e sua base secreta é [DADO_CONFIDENCIAL].",
  "vetor_dimensao": 768,
  "mensagens": "Documento sanitizado via DLP e armazenado no Firestore Vector Search."
}
```

---

## 2. Endpoint: `POST /api/v1/query`

### Payload de Entrada:
```json
{
  "pergunta": "Onde fica a base do Batman?",
  "top_k": 3
}
```

### Resposta esperada (HTTP 200):
```json
{
  "pergunta": "Onde fica a base do Batman?",
  "resposta_gerada": "De acordo com as fichas anonimizadas, a base secreta está localizada em [DADO_CONFIDENCIAL].",
  "documentos_relacionados": [
    {
      "documento_id": "hero-001",
      "score_similaridade": 0.92,
      "conteudo_sanitizado": "[DADO_CONFIDENCIAL] mora em [DADO_CONFIDENCIAL] e sua base secreta é [DADO_CONFIDENCIAL]."
    }
  ]
}
```
