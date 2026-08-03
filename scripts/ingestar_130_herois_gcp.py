import os
import json
import time
import requests

# Segurança: NÃO deixar a chave hardcoded no repositório.
# Para testes locais ou integração manual, gere uma chave temporária e exporte via env var:
# export APP_API_KEY="sua_chave_temporaria"

API_URL = "https://api-rag-seguro-3jjpib7fzq-uc.a.run.app/api/v1/ingest"
API_KEY = os.environ.get("APP_API_KEY", "local-test-key")  # 'local-test-key' apenas para dev local; não commitar chaves reais
HEADERS = {
    "Content-Type": "application/json",
    "X-API-Key": API_KEY
}


def ingestar_todos_herois():
    dataset_path = os.path.join(os.path.dirname(__file__), "../.sandbox/hero_dataset_mock.json")
    with open(dataset_path, "r", encoding="utf-8") as f:
        herois = json.load(f)

    print(f"🚀 Carregando e Ingerindo {len(herois)} herois na nuvem real GCP Cloud Run...")
    
    sucesso = 0
    erros = 0
    inicio = time.time()

    for idx, heroi in enumerate(herois, 1):
        conteudo = heroi["biografia"]
        sigilos = heroi.get("dados_sigilosos", {})
        for k, v in sigilos.items():
            conteudo += f" {k}: {v}"

        payload = {
            "documento_id": heroi["id"],
            "titulo": f"Ficha {heroi['nome_heroi']}",
            "conteudo_bruto": conteudo
        }

        try:
            resp = requests.post(API_URL, json=payload, headers=HEADERS, timeout=10)
            if resp.status_code == 200:
                sucesso += 1
                if idx % 15 == 0 or idx == len(herois):
                    print(f"   ✅ [{idx}/{len(herois)}] Heróis ingestados com sucesso...")
            else:
                erros += 1
                print(f"   ❌ Erro no herói {heroi['id']}: Status {resp.status_code}")
        except Exception as e:
            erros += 1
            print(f"   ❌ Exceção ao enviar {heroi['id']}: {e}")

    tempo = time.time() - inicio
    print(f"\n✨ Carga Massiva Concluída!")
    print(f"   • Sucesso: {sucesso}/{len(herois)}")
    print(f"   • Erros: {erros}")
    print(f"   • Tempo Total: {tempo:.2f}s")


if __name__ == "__main__":
    ingestar_todos_herois()
