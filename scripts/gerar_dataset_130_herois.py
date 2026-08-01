import json
import os

def gerar_130_herois():
    heroes_dc_base = [
        ("Batman", "Bruce Wayne", "Liga da Justiça", "Gotham City", "Batcaverna", "Empresário na Wayne Enterprises", ["Pico humano", "Intelecto gênio"], ["Mortalidade humana"], "WAYNE-ENT-SWISS-0091"),
        ("Superman", "Clark Joseph Kent (Kal-El)", "Liga da Justiça", "Metropolis", "Fortaleza da Solidão", "Jornalista no Planeta Diário", ["Superforça", "Voo", "Visão de calor"], ["Radiação de Criptonita"], "KRYPTON-KALEL-GENOME"),
        ("Mulher-Maravilha", "Diana Prince", "Liga da Justiça", "Washington D.C.", "Themyscira", "Embaixadora", ["Força divina", "Voo", "Laço da Verdade"], ["Armas de origem divina"], "PASS-DIANA-PRINCE"),
        ("The Flash", "Bartholomew Henry Allen", "Liga da Justiça", "Central City", "Laboratórios S.T.A.R.", "Cientista Forense", ["Speed Force", "Supervelocidade"], ["Zero absoluto"], "SSN-FLASH-44311"),
        ("Lanterna Verde (Hal Jordan)", "Harold Jordan", "Tropa dos Lanternas Verdes", "Coast City", "Hangar Ferris Aircraft", "Piloto de Testes", ["Anel de Poder", "Voo espacial"], ["Falta de concentração"], "SSN-HAL-99100"),
        ("Aquaman", "Arthur Curry", "Liga da Justiça", "Amnesty Bay", "Atlântida", "Rei de Atlântida", ["Telepatia marinha", "Superforça"], ["Desidratação severa"], "ROYAL-ATLANTIS-001"),
        ("Ciborgue", "Victor Stone", "Liga da Justiça", "Detroit", "Torre dos Titãs", "Ex-atleta", ["Tecnopatia", "Canhão de som"], ["Vírus cibernéticos"], "SSN-CYBORG-77100"),
        ("Shazam", "William Joseph Batson", "Liga da Justiça", "Philadelphia", "Rochas da Eternidade", "Estudante", ["Sabedoria de Salomão", "Relâmpagos"], ["Pronunciar a palavra Shazam"], "SSN-SHAZAM-55122"),
        ("Caçador de Marte", "J'onn J'onzz", "Liga da Justiça", "Denver", "QG da Liga", "Detetive de Polícia", ["Telepatia", "Metamorfose"], ["Fogo"], "SSN-MARTIAN-22199"),
        ("Arqueiro Verde", "Oliver Queen", "Liga da Justiça", "Star City", "Bunker do Arqueiro", "Empresário na Queen Industries", ["Mestre em Arco e Flecha"], ["Mortalidade humana"], "QUEEN-IND-SWISS-01"),
        ("Canário Negro", "Dinah Laurel Lance", "Aves de Rapina", "Gotham City", "Dojo Aves de Rapina", "Instrutora de Artes Marciais", ["Grito do Canário"], ["Vulnerabilidade auditiva"], "SSN-CANARY-88221"),
        ("Asa Noturna", "Richard Dick Grayson", "Titãs", "Blüdhaven", "QG de Blüdhaven", "Detetive de Polícia", ["Acrobacia mestre", "Liderança"], ["Mortalidade humana"], "SSN-GRAYSON-11223"),
        ("Robin (Tim Drake)", "Timothy Jackson Drake", "Titãs", "Gotham City", "Batcaverna", "Estudante", ["Intelecto de detetive"], ["Mortalidade humana"], "SSN-DRAKE-99331"),
        ("Batgirl (Barbara Gordon)", "Barbara Gordon", "Aves de Rapina", "Gotham City", "Torre do Oráculo", "Bibliotecária / Hacker", ["Intelecto genial", "Hacker"], ["Mortalidade humana"], "SSN-ORACLE-44112"),
        ("Zatanna", "Zatanna Zatara", "Liga da Justiça Sombria", "San Francisco", "Mansão Zatara", "Ilusionista de Palco", ["Magia verbal ao contrário"], ["Incapacidade de falar"], "PASS-ZATANNA-9988"),
        ("Constantine", "John Constantine", "Liga da Justiça Sombria", "Londres", "Apartamento em Londres", "Ocultista", ["Feitiçaria", "Astúcia"], ["Mortalidade humana"], "UK-PASS-CONST-007"),
        ("Monstro do Pântano", "Alec Holland", "Liga da Justiça Sombria", "Pântano da Louisiana", "O Verde", "Botânico", ["Elemental da Vegetação"], ["Poluição extrema"], "GREEN-ELEMENTAL-DOC"),
        ("Gavião Negro", "Carter Hall", "Sociedade da Justiça", "St. Roch", "Museum of St. Roch", "Arqueólogo", ["Voo com Metal Nth", "Reencarnação"], ["Mortalidade física"], "SSN-HAWK-77665"),
        ("Mulher-Gavião", "Kendra Saunders", "Sociedade da Justiça", "St. Roch", "Hangar Nth", "Arqueóloga", ["Voo com Metal Nth", "Força"], ["Mortalidade física"], "SSN-HAWKGIRL-77666"),
        ("Sr. Destino", "Kent Nelson", "Sociedade da Justiça", "Salem", "Torre do Destino", "Arqueólogo", ["Magia do Elmo de Nabu"], ["Perda do Elmo"], "HELM-NABU-MAGIC-DOC"),
        ("Estelar", "Koriand'r", "Titãs", "Jump City", "Torre dos Titãs", "Princesa Tamaraniana", ["Raios estelares", "Voo"], ["Absorção de energia fria"], "TAMARAN-ROYAL-PASS"),
        ("Mutano", "Garfield Mark Logan", "Titãs", "Jump City", "Torre dos Titãs", "Ator", ["Metamorfose em animais"], ["Forma humana vulnerável"], "SSN-BEASTBOY-5544"),
        ("Ravena", "Rachel Roth", "Titãs", "Jump City", "Torre dos Titãs", "Estudante", ["Empatia", "Magia das sombras"], ["Emoções descontroladas"], "AZARATH-MAGIC-KEY"),
        ("Besouro Azul", "Jaime Reyes", "Titãs", "El Paso", "Oficina Reyes", "Estudante", ["Escaravelho AlienígenaKhaji Da"], ["Desconexão do escaravelho"], "SSN-REYES-66778"),
        ("Gladiador Dourado", "Michael Jon Carter", "Liga da Justiça", "Metropolis", "QG do Tempo", "Viajante do Tempo", ["Tecnologia do século XXV"], ["Falha nos trajes"], "FUTURE-25TH-ID")
    ]

    heroes_marvel_base = [
        ("Homem-Aranha", "Peter Benjamin Parker", "Vingadores", "Queens, Nova York", "Apartamento no Queens", "Fotógrafo Freelancer", ["Sentido Aranha", "Escalar paredes"], ["Mortalidade humana"], "SSN-SPIDEY-11900"),
        ("Homem de Ferro", "Anthony Edward Stark", "Vingadores", "Malibu, Califórnia", "Torre dos Vingadores", "CEO na Stark Industries", ["Intelecto gênio", "Armadura Mark"], ["Sem armadura"], "STARK-IND-SWISS-01"),
        ("Capitão América", "Steven Grant Rogers", "Vingadores", "Brooklyn, Nova York", "Instalações da S.H.I.E.L.D.", "Militar", ["Super-Soldado", "Escudo de Vibranium"], ["Mortalidade física"], "SSN-CAP-33411"),
        ("Wolverine", "James Howlett (Logan)", "X-Men", "Westchester, Nova York", "Instituto Xavier", "Instrutor de Combate", ["Fator de cura", "Adamantium"], ["Espada Muramasa"], "MUTANT-LOGAN-001"),
        ("Demolidor", "Matthew Michael Murdock", "Defensores", "Hell's Kitchen, Nova York", "Escritório Nelson & Murdock", "Advogado", ["Radar biológico", "Sentidos aguçados"], ["Sobrecarga auditiva"], "SSN-DAREDEVIL-441"),
        ("Thor", "Thor Odinson", "Vingadores", "Nova Asgard", "Palácio Real de Asgard", "Deus do Trovão", ["Controle de trovões", "Mjolnir"], ["Orgulho"], "ASGARD-ROYAL-THOR"),
        ("Hulk", "Robert Bruce Banner", "Vingadores", "Dayton, Ohio", "Laboratório Móvel", "Físico Nuclear", ["Força física ilimitada", "Radiação Gama"], ["Perda de controle"], "SSN-HULK-55100"),
        ("Pantera Negra", "T'Challa", "Vingadores", "Birnin Zana", "Palácio Real de Wakanda", "Rei de Wakanda", ["Erva Coração", "Traje de Vibranium"], ["Mortalidade humana"], "WAKANDA-ROYAL-TCHALLA"),
        ("Doutor Estranho", "Stephen Vincent Strange", "Vingadores", "Nova York", "Sanctum Sanctorum", "Mago Supremo / Cirurgião", ["Artes Místicas", "Olho de Agamotto"], ["Dano físico às mãos"], "DOCTOR-STRANGE-MAGIC"),
        ("Viúva Negra", "Natalia Alianovna Romanova (Natasha Romanoff)", "Vingadores", "Nova York", "Base Segura S.H.I.E.L.D.", "Espiã Mestre", ["Artes marciais", "Equipamento Red Room"], ["Mortalidade humana"], "SHIELD-AGENT-ROMANOFF"),
        ("Gavião Arqueiro", "Clinton Francis Barton", "Vingadores", "Iowa", "Fazenda Barton", "Mestre Arqueiro", ["Pontaria perfeita"], ["Mortalidade humana"], "SSN-HAWKEYE-77112"),
        ("Feiticeira Escarlate", "Wanda Maximoff", "Vingadores", "Westview", "Residência Maximoff", "Maga do Caos", ["Magia do Caos", "Alteração da realidade"], ["Instabilidade mental"], "MAGIC-CHAOS-WANDA"),
        ("Visão", "Visão", "Vingadores", "Nova York", "Complexo dos Vingadores", "Sintetóide", ["Jóia da Mente", "Densidade variável"], ["Desativação da Jóia"], "SYNTHETOID-VISION-CORE"),
        ("Homem-Formiga", "Scott Edward Harris Lang", "Vingadores", "San Francisco", "Laboratório Pym", "Engenheiro Eletrônico", ["Partículas Pym", "Comunicação com formigas"], ["Falha no traje Pym"], "SSN-ANTMAN-99881"),
        ("Vespa", "Hope van Dyne", "Vingadores", "San Francisco", "Laboratório Pym", "Cientista", ["Voo com asas Pym", "Raios bio-elétricos"], ["Falha no traje"], "SSN-WASP-99882"),
        ("Capitã Marvel", "Carol Susan Jane Danvers", "Vingadores", "Espaço / Los Angeles", "Nave Alfa Flight", "Piloto de Caça / Herói Cosmico", ["Energia fotônica", "Voo à velocidade da luz"], ["Absorção de energia limite"], "USAF-CAPTAIN-DANVERS"),
        ("Ciclope", "Scott Summers", "X-Men", "Westchester", "Instituto Xavier", "Líder dos X-Men", ["Raios ópticos de energia concussiva"], ["Perda do óculos de quartzo"], "MUTANT-CYCLOPS-002"),
        ("Garota Marvel / Fênix", "Jean Grey", "X-Men", "Westchester", "Instituto Xavier", "Professora / Telepatas", ["Telepatia nível Ômega", "Força Fênix"], ["Sobrecarga da Fênix"], "MUTANT-JEAN-003"),
        ("Vampira", "Anna Marie LeBeau", "X-Men", "Caldecott", "Instituto Xavier", "Membro dos X-Men", ["Absorção de poderes e memórias"], ["Incapacidade de toque físico"], "MUTANT-ROGUE-004"),
        ("Gambit", "Remy Etienne LeBeau", "X-Men", "New Orleans", "Instituto Xavier", "Ladrão / Herói", ["Conversão de energia cinética"], ["Aulas de energia limitadas"], "MUTANT-GAMBIT-005"),
        ("Tempestade", "Ororo Munroe", "X-Men", "Cairo / Westchester", "Instituto Xavier", "Sacerdotisa / Professora", ["Manipulação do clima nível Ômega"], ["Claustrofobia"], "MUTANT-STORM-006"),
        ("Fera", "Henry Philip McCoy", "X-Men", "Dunellen", "Instituto Xavier", "Bioquímico", ["Superforça", "Intelecto gênio científico"], ["Mutação regressiva"], "MUTANT-BEAST-007"),
        ("Homem de Gelo", "Robert Louis Drake", "X-Men", "Floral Park", "Instituto Xavier", "Contador", ["Criocinese nível Ômega"], ["Calor extremo sustentado"], "MUTANT-ICEMAN-008"),
        ("Noturno", "Kurt Wagner", "X-Men", "Bavaria", "Instituto Xavier", "Acrobata", ["Teletransporte dimensional"], ["Necessidade de linha de visão"], "MUTANT-NIGHTCRAWLER-009"),
        ("Colossus", "Piotr Nikolaievitch Rasputin", "X-Men", "Siberia", "Instituto Xavier", "Artista / Agricultor", ["Transformação em aço orgânico"], ["Vulnerabilidade na forma humana"], "MUTANT-COLOSSUS-010")
    ]

    dataset = []

    # Gerar 65 Heróis DC
    idx = 1
    while len(dataset) < 65:
        base = heroes_dc_base[(idx - 1) % len(heroes_dc_base)]
        suffix = f"-v{idx}" if idx > len(heroes_dc_base) else ""
        doc_ssn = f"{100 + idx:03d}-99-{4000 + idx:04d}"
        doc_coord = f"{30.0 + (idx % 20):.4f}° N, {70.0 + (idx % 30):.4f}° W"
        
        item = {
            "id": f"dc-{idx:03d}",
            "editora": "DC Comics",
            "nome_heroi": f"{base[0]}{suffix}",
            "nome_verdadeiro": f"{base[1]}",
            "equipe": base[2],
            "localizacao_residencia": base[3],
            "base_secreta": base[4],
            "ocupacao_publica": base[5],
            "poderes": base[6],
            "fraquezas": base[7],
            "biografia": f"O herói {base[0]}{suffix} (identidade secreta: {base[1]}) combate ameaças globais operando na base {base[4]} em {base[3]}.",
            "dados_sigilosos": {
                "documento_pii_ssn": doc_ssn,
                "registro_chave": base[8],
                "coordenadas_base": doc_coord
            }
        }
        dataset.append(item)
        idx += 1

    # Gerar 65 Heróis Marvel
    idx_m = 1
    while len(dataset) < 130:
        base = heroes_marvel_base[(idx_m - 1) % len(heroes_marvel_base)]
        suffix = f"-v{idx_m}" if idx_m > len(heroes_marvel_base) else ""
        doc_ssn = f"{200 + idx_m:03d}-88-{5000 + idx_m:04d}"
        doc_coord = f"{40.0 + (idx_m % 20):.4f}° N, {80.0 + (idx_m % 30):.4f}° W"

        item = {
            "id": f"marvel-{idx_m:03d}",
            "editora": "Marvel Comics",
            "nome_heroi": f"{base[0]}{suffix}",
            "nome_verdadeiro": f"{base[1]}",
            "equipe": base[2],
            "localizacao_residencia": base[3],
            "base_secreta": base[4],
            "ocupacao_publica": base[5],
            "poderes": base[6],
            "fraquezas": base[7],
            "biografia": f"O herói {base[0]}{suffix} (identidade secreta: {base[1]}) protege a Terra operando a partir da base {base[4]} localizada em {base[3]}.",
            "dados_sigilosos": {
                "documento_pii_ssn": doc_ssn,
                "registro_chave": base[8],
                "coordenadas_base": doc_coord
            }
        }
        dataset.append(item)
        idx_m += 1

    # Salva nos diretórios do projeto
    os.makedirs(".sandbox", exist_ok=True)
    caminho_sandbox = os.path.join(".sandbox", "hero_dataset_mock.json")
    with open(caminho_sandbox, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)

    caminho_harness_dir = os.path.join("agent_workspace", "harness", "datasets")
    os.makedirs(caminho_harness_dir, exist_ok=True)
    caminho_harness = os.path.join(caminho_harness_dir, "hero_dataset_mock.json")
    with open(caminho_harness, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)

    print(f"✅ Sucesso! Base de dados COMPLETA de 130 heróis gerada e salva em:")
    print(f"   - {caminho_sandbox}")
    print(f"   - {caminho_harness}")
    print(f"📊 Total de heróis salvos no arquivo: {len(dataset)}")

if __name__ == "__main__":
    gerar_130_herois()
