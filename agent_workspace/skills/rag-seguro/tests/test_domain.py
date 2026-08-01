from src.domain.entities import DocumentoBruto, DocumentoSanitizado
from src.domain.rules import LocalPIIRules

def test_documento_bruto_criacao():
    doc = DocumentoBruto(
        documento_id="hero-001",
        titulo="Ficha Batman",
        conteudo_bruto="Bruce Wayne mora em Gotham City"
    )
    assert doc.documento_id == "hero-001"
    assert "Bruce Wayne" in doc.conteudo_bruto

def test_local_pii_rules_sanitizacao_batman():
    texto = "Bruce Wayne mora em Gotham e sua base é a Batcaverna"
    texto_sanitizado, piis = LocalPIIRules.sanitizar_localmente(texto)
    assert "[DADO_CONFIDENCIAL]" in texto_sanitizado
    assert "bruce wayne" in piis
    assert "batcaverna" in piis

def test_local_pii_rules_sanitizacao_spiderman():
    texto = "Peter Parker mora no Queens"
    texto_sanitizado, piis = LocalPIIRules.sanitizar_localmente(texto)
    assert texto_sanitizado == "[DADO_CONFIDENCIAL] mora no [DADO_CONFIDENCIAL]"
    assert "peter parker" in piis
    assert "queens" in piis
