# 📋 Plano 000: Sandbox & Ambiente de Validação Local

## Objetivo
Configurar o ambiente de desenvolvimento local, mocks dos SDKs da GCP (`google.cloud.dlp_v2`, `google.cloud.firestore`, `vertexai`) e dataset fictício da DC/Marvel para permitir desenvolvimento TDD sem custos de nuvem.

## Checkpoints de Conclusão:
- [x] Dataset mock `hero_dataset_mock.json` criado com 5 fichas de heróis contendo PII.
- [x] Fixtures e Mocks configurados em `tests/conftest.py`.
- [x] Validação da suíte `pytest` executando sem erros offline.
