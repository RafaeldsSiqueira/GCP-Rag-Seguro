import re
from typing import List, Tuple

class LocalPIIRules:
    """Regras determinísticas de fallback/validação local para PII (DC & Marvel)."""
    
    NOMES_CIVIS_PII = [
        "bruce wayne", "clark joseph kent", "clark kent", "kal-el", "diana prince",
        "bartholomew henry allen", "barry allen", "harold jordan", "hal jordan",
        "arthur curry", "victor stone", "william joseph batson", "billy batson",
        "j'onn j'onzz", "peter benjamin parker", "peter parker", "anthony edward stark",
        "tony stark", "steven grant Rogers", "steve rogers", "james howlett", "logan",
        "matthew michael murdock", "matt murdock", "thor odinson", "robert bruce banner",
        "bruce banner", "t'challa"
    ]

    LOCAIS_SENSIVEIS_PII = [
        "batcaverna", "mansao wayne", "fortaleza da solidao", "themyscira",
        "laboratorios s.t.a.r.", "hangar ferris aircraft", "atlantida", "torre dos titas",
        "rochas da eternidade", "qg da liga", "apartamento no queens", "torre dos vingadores",
        "instalacoes da s.h.i.e.l.d.", "instituto xavier", "escritorio nelson & murdock",
        "palacio real de asgard", "laboratorio movel", "palacio real de wakanda",
        "gotham city", "gotham", "queens", "metropolis", "malibu"
    ]

    # Expressões Regulares para PIIs Estruturadas (SSNs, Passaportes, Coordenadas, Contas)
    PADROES_REGEX_PII = [
        (re.compile(r'\b\d{3}-\d{2}-\d{4}\b'), "[SSN_CONFIDENCIAL]"),
        (re.compile(r'\b[A-Z]{3,7}-[A-Z0-9-]+\b'), "[DOC_CONFIDENCIAL]"),
        (re.compile(r'\b\d{1,3}\.\d+°\s*[NS],\s*\d{1,3}\.\d+°\s*[WE]\b'), "[COORDENADAS_CONFIDENCIAIS]")
    ]

    @classmethod
    def sanitizar_localmente(cls, texto: str) -> Tuple[str, List[str]]:
        texto_sanitizado = texto
        piis_encontradas = []

        # 1. Aplica sanitização via Regex para SSNs, Passaportes e Coordenadas
        for regex_padrao, tag_substituicao in cls.PADROES_REGEX_PII:
            matches = regex_padrao.findall(texto_sanitizado)
            if matches:
                piis_encontradas.extend(matches)
                texto_sanitizado = regex_padrao.sub(tag_substituicao, texto_sanitizado)

        # 2. Aplica sanitização por nomes civis e locais
        todos_termos = cls.NOMES_CIVIS_PII + cls.LOCAIS_SENSIVEIS_PII
        for termo in todos_termos:
            padrao = re.compile(re.escape(termo), re.IGNORECASE)
            if padrao.search(texto_sanitizado):
                piis_encontradas.append(termo)
                texto_sanitizado = padrao.sub("[DADO_CONFIDENCIAL]", texto_sanitizado)

        return texto_sanitizado, piis_encontradas

    @classmethod
    def converter_para_tipos_info(cls, piis_raw: List[str]) -> List[str]:
        tipos_set = set()
        for p in piis_raw:
            p_str = str(p).lower()
            if "-" in p_str and any(c.isdigit() for c in p_str):
                tipos_set.add("US_SOCIAL_SECURITY_NUMBER")
            elif "°" in p_str:
                tipos_set.add("LOCATION_COORDINATES")
            elif any(word in p_str for word in ["swiss", "pass", "id", "genome"]):
                tipos_set.add("FINANCIAL_DOCUMENT")
            elif any(word in p_str for word in cls.LOCAIS_SENSIVEIS_PII):
                tipos_set.add("LOCATION")
            else:
                tipos_set.add("PERSON_NAME")
        return sorted(list(tipos_set)) if tipos_set else ["PERSON_NAME", "LOCATION"]
