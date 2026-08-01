# 🗄️ Especificação de Schema do Firestore Vector Search

## Coleção: `fichas_sanitizadas`

### Documento Schema:
```json
{
  "documento_id": "string",
  "titulo": "string",
  "conteudo_sanitizado": "string",
  "embedding": "array[float] (768 dimensões)",
  "criado_em": "timestamp ISO-8601",
  "metadata": {
    "sanitizado_por": "Cloud DLP",
    "cost_center": "cc-ia-genai-042"
  }
}
```

### Índice Vetorial Firestore:
* **Coleção:** `fichas_sanitizadas`
* **Campo de Vetor:** `embedding`
* **Medida de Distância:** COSINE (Similaridade por Cosseno)
* **Dimensão:** 768
