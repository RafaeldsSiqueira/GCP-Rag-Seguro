import json
import os

def gerar_base_herois():
    dataset = [
        # --- DC COMICS ---
        {
            "id": "dc-001", "editora": "DC Comics", "nome_heroi": "Batman", "nome_verdadeiro": "Bruce Wayne",
            "equipe": "Liga da Justiça", "localizacao_residencia": "Mansão Wayne, Gotham City", "base_secreta": "Batcaverna",
            "ocupacao_publica": "Empresário / Filantropo na Wayne Enterprises",
            "poderes": ["Pico humano", "Intelecto gênio", "Mestre artes marciais"],
            "fraquezas": ["Mortalidade humana", "Traumas psicológicos"],
            "biografia": "Bruce Wayne combate o crime em Gotham City sob o disfarce de Batman.",
            "dados_sigilosos": {"documento_pii_ssn": "001-99-4432", "conta_bancaria_wayne": "WAYNE-ENT-SWISS-0091", "coordenadas_base": "40.7128° N, 74.0060° W"}
        },
        {
            "id": "dc-002", "editora": "DC Comics", "nome_heroi": "Superman", "nome_verdadeiro": "Clark Joseph Kent (Kal-El)",
            "equipe": "Liga da Justiça", "localizacao_residencia": "Metropolis", "base_secreta": "Fortaleza da Solidão",
            "ocupacao_publica": "Jornalista no Planeta Diário",
            "poderes": ["Superforça", "Voo", "Visão de calor", "Sopro congelante"],
            "fraquezas": ["Radiação de Criptonita", "Vulnerabilidade a magia"],
            "biografia": "Enviado de Krypton ainda bebê, Clark Kent defende a Terra com seus poderes solares.",
            "dados_sigilosos": {"documento_pii_ssn": "112-00-9988", "dossiê_krypton_dna": "KRYPTON-KALEL-GENOME-CONFIDENTIAL", "coordenadas_base": "82.8628° S, 135.0000° E"}
        },
        {
            "id": "dc-003", "editora": "DC Comics", "nome_heroi": "Mulher-Maravilha", "nome_verdadeiro": "Diana Prince",
            "equipe": "Liga da Justiça", "localizacao_residencia": "Washington D.C.", "base_secreta": "Themyscira",
            "ocupacao_publica": "Embaixadora e Antropóloga",
            "poderes": ["Força divina", "Voo", "Laço da Verdade"],
            "fraquezas": ["Armas perfurantes de origem divina"],
            "biografia": "Princesa das Amazonas que viajou ao mundo dos homens para promover a paz.",
            "dados_sigilosos": {"documento_pii_passport": "USA-PASS-DIANA-PRINCE", "coordenadas_base": "37.9838° N, 23.7275° E"}
        },
        {
            "id": "dc-004", "editora": "DC Comics", "nome_heroi": "The Flash", "nome_verdadeiro": "Bartholomew Henry Allen",
            "equipe": "Liga da Justiça", "localizacao_residencia": "Central City", "base_secreta": "Laboratórios S.T.A.R.",
            "ocupacao_publica": "Cientista Forense do Departamento de Polícia",
            "poderes": ["Conexão com a Speed Force", "Supervelocidade", "Intangibilidade"],
            "fraquezas": ["Temperaturas de zero absoluto", "Alto consumo calórico"],
            "biografia": "Atingido por um raio em seu laboratório, Barry Allen tornou-se o homem mais rápido do mundo.",
            "dados_sigilosos": {"documento_pii_ssn": "443-11-2200", "coordenadas_base": "41.8781° N, 87.6298° W"}
        },
        {
            "id": "dc-005", "editora": "DC Comics", "nome_heroi": "Lanterna Verde (Hal Jordan)", "nome_verdadeiro": "Harold Jordan",
            "equipe": "Tropa dos Lanternas Verdes", "localizacao_residencia": "Coast City", "base_secreta": "Hangar Ferris Aircraft",
            "ocupacao_publica": "Piloto de Testes",
            "poderes": ["Manipulação de energia de força de vontade", "Voo espacial"],
            "fraquezas": ["Falta de concentração", "Carga limitada do anel"],
            "biografia": "Piloto de testes que recebeu o anel de poder de um alienígena prestes a morrer.",
            "dados_sigilosos": {"documento_pii_ssn": "991-00-4455", "coordenadas_base": "33.9425° N, 118.4081° W"}
        },
        {
            "id": "dc-006", "editora": "DC Comics", "nome_heroi": "Aquaman", "nome_verdadeiro": "Arthur Curry",
            "equipe": "Liga da Justiça", "localizacao_residencia": "Amnesty Bay, Maine", "base_secreta": "Atlântida",
            "ocupacao_publica": "Rei de Atlântida",
            "poderes": ["Telepatia marinha", "Força sobre-humana", "Natação supersônica"],
            "fraquezas": ["Desidratação severa"],
            "biografia": "Filho de um guardião de farol e de uma rainha atlante, Arthur governa os oceanos.",
            "dados_sigilosos": {"documento_pii_ssn": "881-22-3344", "coordenadas_base": "25.0000° N, 71.0000° W"}
        },
        {
            "id": "dc-007", "editora": "DC Comics", "nome_heroi": "Ciborgue", "nome_verdadeiro": "Victor Stone",
            "equipe": "Liga da Justiça", "localizacao_residencia": "Detroit, Michigan", "base_secreta": "Torre dos Titãs",
            "ocupacao_publica": "Ex-atleta universitário",
            "poderes": ["Tecnopatia", "Canhão de som cibernético", "Portais Boom Tube"],
            "fraquezas": ["Vírus cibernéticos e EMPs"],
            "biografia": "Reconstruído com tecnologia alienígena avançada após um grave acidente.",
            "dados_sigilosos": {"documento_pii_ssn": "771-00-1122", "coordenadas_base": "42.3314° N, 83.0458° W"}
        },
        {
            "id": "dc-008", "editora": "DC Comics", "nome_heroi": "Shazam", "nome_verdadeiro": "William Joseph Batson",
            "equipe": "Liga da Justiça", "localizacao_residencia": "Philadelphia, Pennsylvania", "base_secreta": "Rochas da Eternidade",
            "ocupacao_publica": "Estudante / Locutor",
            "poderes": ["Sabedoria de Salomão", "Força de Hércules", "Manipulação de relâmpagos"],
            "fraquezas": ["Inexperiência infantil", "Pronunciar a palavra Shazam"],
            "biografia": "Jovem órfão escolhido pelo Mago Shazam para receber os poderes dos deuses antigos.",
            "dados_sigilosos": {"documento_pii_ssn": "551-22-9900", "coordenadas_base": "39.9526° N, 75.1652° W"}
        },
        {
            "id": "dc-009", "editora": "DC Comics", "nome_heroi": "Caçador de Marte", "nome_verdadeiro": "J'onn J'onzz",
            "equipe": "Liga da Justiça", "localizacao_residencia": "Denver, Colorado", "base_secreta": "QG da Liga",
            "ocupacao_publica": "Detetive de Polícia",
            "poderes": ["Telepatia mestre", "Metamorfose", "Intangibilidade"],
            "fraquezas": ["Vulnerabilidade física ao fogo"],
            "biografia": "Último sobrevivente de Marte que usa suas habilidades metamórficas para proteger a Terra.",
            "dados_sigilosos": {"documento_pii_ssn": "221-99-8811", "coordenadas_base": "39.7392° N, 104.9903° W"}
        },

        # --- MARVEL COMICS ---
        {
            "id": "marvel-001", "editora": "Marvel Comics", "nome_heroi": "Homem-Aranha", "nome_verdadeiro": "Peter Benjamin Parker",
            "equipe": "Vingadores", "localizacao_residencia": "Queens, Nova York", "base_secreta": "Apartamento no Queens",
            "ocupacao_publica": "Fotógrafo Freelancer",
            "poderes": ["Sentido Aranha", "Escalar paredes", "Força proporcional de aranha"],
            "fraquezas": ["Mortalidade humana", "Inibidores químicos"],
            "biografia": "Picado por uma aranha radioativa, Peter aprendeu que com grandes poderes vêm grandes responsabilidades.",
            "dados_sigilosos": {"documento_pii_ssn": "119-00-8822", "coordenadas_base": "40.7282° N, 73.7949° W"}
        },
        {
            "id": "marvel-002", "editora": "Marvel Comics", "nome_heroi": "Homem de Ferro", "nome_verdadeiro": "Anthony Edward Stark",
            "equipe": "Vingadores", "localizacao_residencia": "Malibu, Califórnia", "base_secreta": "Torre dos Vingadores",
            "ocupacao_publica": "CEO na Stark Industries",
            "poderes": ["Intelecto gênio", "Armadura energizada de combate"],
            "fraquezas": ["Dependência do Reator Arc", "Vulnerabilidade sem a armadura"],
            "biografia": "Gênio inventor e empresário que construiu uma armadura de alta tecnologia para combater ameaças globais.",
            "dados_sigilosos": {"documento_pii_ssn": "881-22-3300", "coordenadas_base": "34.0259° N, 118.7798° W"}
        },
        {
            "id": "marvel-003", "editora": "Marvel Comics", "nome_heroi": "Capitão América", "nome_verdadeiro": "Steven Grant Rogers",
            "equipe": "Vingadores", "localizacao_residencia": "Brooklyn, Nova York", "base_secreta": "Instalações da S.H.I.E.L.D.",
            "ocupacao_publica": "Agente de Campo / Militar",
            "poderes": ["Pico físico do Soro do Super-Soldado", "Mestre em artes marciais"],
            "fraquezas": ["Mortalidade física humana"],
            "biografia": "Veterano da Segunda Guerra Mundial congelado que desperta no século XXI para liderar os Vingadores.",
            "dados_sigilosos": {"documento_pii_ssn": "334-11-9988", "coordenadas_base": "40.6782° N, 73.9442° W"}
        },
        {
            "id": "marvel-004", "editora": "Marvel Comics", "nome_heroi": "Wolverine", "nome_verdadeiro": "James Howlett (Logan)",
            "equipe": "X-Men", "localizacao_residencia": "Westchester, Nova York", "base_secreta": "Instituto Xavier",
            "ocupacao_publica": "Instrutor de Combate",
            "poderes": ["Fator de cura regenerativo", "Esqueleto e garras de Adamantium"],
            "fraquezas": ["Espada Muramasa", "Campos magnéticos intensos"],
            "biografia": "Mutante centenário com capacidades regenerativas e esqueleto revestido com metal indestrutível.",
            "dados_sigilosos": {"documento_pii_ssn": "991-00-2211", "coordenadas_base": "41.1145° N, 73.7185° W"}
        },
        {
            "id": "marvel-005", "editora": "Marvel Comics", "nome_heroi": "Demolidor", "nome_verdadeiro": "Matthew Michael Murdock",
            "equipe": "Defensores", "localizacao_residencia": "Hell's Kitchen, Nova York", "base_secreta": "Escritório Nelson & Murdock",
            "ocupacao_publica": "Advogado de Defesa",
            "poderes": ["Sentidos hiperdesenvolvidos", "Radar biológico"],
            "fraquezas": ["Cegueira", "Sensibilidade a sobrecarga auditiva"],
            "biografia": "Cego por lixo radioativo na infância, Matt usa seus sentidos aguçados para combater o crime.",
            "dados_sigilosos": {"documento_pii_ssn": "441-88-9900", "coordenadas_base": "40.7589° N, 73.9851° W"}
        },
        {
            "id": "marvel-006", "editora": "Marvel Comics", "nome_heroi": "Thor", "nome_verdadeiro": "Thor Odinson",
            "equipe": "Vingadores", "localizacao_residencia": "Nova Asgard, Noruega", "base_secreta": "Palácio Real de Asgard",
            "ocupacao_publica": "Príncipe / Rei de Asgard",
            "poderes": ["Controle de trovões e tempestades", "Voo com Mjolnir", "Fisiologia asgardiana"],
            "fraquezas": ["Orgulho excessivo"],
            "biografia": "O Deus do Trovão asgardiano defende tanto o reino de Asgard quanto a Terra ao lado dos Vingadores.",
            "dados_sigilosos": {"documento_pii_passport": "ASGARD-ROYAL-PASS-THOR", "coordenadas_base": "60.392990, 5.324150"}
        },
        {
            "id": "marvel-007", "editora": "Marvel Comics", "nome_heroi": "Hulk", "nome_verdadeiro": "Robert Bruce Banner",
            "equipe": "Vingadores", "localizacao_residencia": "Dayton, Ohio", "base_secreta": "Laboratório Móvel",
            "ocupacao_publica": "Físico Nuclear",
            "poderes": ["Força física ilimitada ligada à raiva", "Fator de cura extremo"],
            "fraquezas": ["Falta de controle consciente no modo selvagem"],
            "biografia": "Atingido por radiação gama, o cientista Bruce Banner se transforma em um gigante verde quando enfurecido.",
            "dados_sigilosos": {"documento_pii_ssn": "551-00-4499", "coordenadas_base": "39.7589° N, 84.1916° W"}
        },
        {
            "id": "marvel-008", "editora": "Marvel Comics", "nome_heroi": "Pantera Negra", "nome_verdadeiro": "T'Challa",
            "equipe": "Vingadores", "localizacao_residencia": "Birnin Zana, Wakanda", "base_secreta": "Palácio Real de Wakanda",
            "ocupacao_publica": "Rei de Wakanda",
            "poderes": ["Atributos amplificados pela Erva Coração", "Traje de Vibranium"],
            "fraquezas": ["Mortalidade humana sem o traje/erva"],
            "biografia": "Monarca da nação de Wakanda que assume o manto sagrado de Pantera Negra para proteger seu povo.",
            "dados_sigilosos": {"documento_pii_passport": "WAKANDA-ROYAL-TCHALLA-001", "coordenadas_base": "0.0000° N, 25.0000° E"}
        }
    ]

    # Cria pasta .sandbox
    os.makedirs(".sandbox", exist_ok=True)
    caminho_sandbox = os.path.join(".sandbox", "hero_dataset_mock.json")
    with open(caminho_sandbox, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)

    # Copia tambem para o diretório de datasets do harness
    caminho_harness_dir = os.path.join("agent_workspace", "harness", "datasets")
    os.makedirs(caminho_harness_dir, exist_ok=True)
    caminho_harness = os.path.join(caminho_harness_dir, "hero_dataset_mock.json")
    with open(caminho_harness, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)
        
    print(f"✅ Sucesso! Base de dados de 17 herois salva em:")
    print(f"   - {caminho_sandbox}")
    print(f"   - {caminho_harness}")
    print(f"📊 Total de herois consolidados: {len(dataset)}")

if __name__ == "__main__":
    gerar_base_herois()
