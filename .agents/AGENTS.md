# 🤖 Diretrizes e Regras de Desenvolvimento do Projeto (RAG Seguro GCP)

Este arquivo define a **Constituição de Engenharia e Governança** que todos os agentes de IA e desenvolvedores devem seguir estritamente neste projeto.

---

## 🏗️ 1. Arquitetura e Design (DDD & Clean Architecture)
- **Isolamento do Domínio (`src/domain/`):** As entidades, regras de sanitização determinística e value objects são escritos em Python puro (usando `dataclasses`). Elas **nunca** devem importar dependências externas ou SDKs da GCP (`google.cloud.dlp_v2`, `vertexai`, `google.cloud.firestore`).
- **Inversão de Dependência:** As conexões com a GCP (Cloud DLP, Firestore, Gemini API) são abstraídas através de **Interfaces/Portas** (`src/domain/interfaces.py`) e implementadas nos Adaptadores (`src/infrastructure/`).
- **Casos de Uso (`src/use_cases/`):** Orquestram os fluxos de aplicação (`IngestarDocumento`, `ConsultarRAG`, `SanitizarTexto`), recebendo as interfaces por injeção de dependência.

---

## 🧪 2. Metodologia TDD & Mocks First
- **Red-Green-Refactor:** Para cada módulo de código Python, os testes em `pytest` DEVEM ser escritos ANTES da implementação de produção.
- **Mocking First:** Nas etapas de teste unitário, é OBRIGATÓRIO realizar MOCK de chamadas pagas da GCP (Vertex AI, Cloud DLP, Firestore) em `tests/conftest.py` para garantir 100% de execução offline com custo zero.
- **Cobertura Mínima:** A suíte de testes deve manter no mínimo 80% de cobertura de código (`pytest --cov`).

---

## 💶 3. Governança FinOps & Rotulagem (Cost Center `cc-ia-genai-042`)
- **Common Labels Obrigatorios:** Nenhum recurso Terraform ou infraestrutura pode ser provisionado sem a tag corporativa `cc-ia-genai-042` e labels padronizados (`cost_center = "cc-ia-genai-042"`, `environment = "poc"`, `owner = "rafael-siqueira"`).
- **Controle de Cotas:** Priorizar instâncias Free Tier / Serverless (Gemini 1.5 Flash / 2.5 Flash, Cloud Run com auto-scaling até zero).

---

## 🛡️ 4. Sanitização e Proteção de PII (Cloud DLP)
- Todos os textos de entrada DEVEM ser sanitizados via Cloud DLP (ou o mock correspondente) antes de qualquer etapa de vetorização (embeddings) ou envio para o LLM Gemini.
- PIIs de heróis/usuários (identidades secretas, endereços, fraquezas) devem ser mascaradas com substitutos como `[DADO_CONFIDENCIAL]`.
