from src.domain.entities import DocumentoBruto
from src.infrastructure.dlp_sanitizer import CloudDLPSanitizer

def test_sanitizador_peter_parker_queens(fake_dlp):
    doc_bruto = DocumentoBruto(
        documento_id="spidey-01",
        titulo="Spiderman Ficha",
        conteudo_bruto="Peter Parker mora no Queens"
    )
    
    sanitizer = CloudDLPSanitizer(dlp_client_adapter=fake_dlp)
    doc_sanitizado = sanitizer.sanitizar(doc_bruto)
    
    assert doc_sanitizado.documento_id == "spidey-01"
    assert doc_sanitizado.conteudo_sanitizado == "[DADO_CONFIDENCIAL] mora no [DADO_CONFIDENCIAL]"
    assert doc_sanitizado.cost_center == "cc-ia-genai-042"

def test_sanitizador_batch_processamento(fake_dlp):
    sanitizer = CloudDLPSanitizer(dlp_client_adapter=fake_dlp)
    textos = [
        "Bruce Wayne mora em Gotham",
        "Tony Stark mora em Malibu"
    ]
    resultados = sanitizer.sanitizar_lote(textos)
    assert len(resultados) == 2
    assert "[DADO_CONFIDENCIAL] mora em [DADO_CONFIDENCIAL]" in resultados[0]
    assert "[DADO_CONFIDENCIAL] mora em [DADO_CONFIDENCIAL]" in resultados[1]

def test_sanitizacao_base_completa_130_herois(fake_dlp, dataset_mock_herois):
    assert len(dataset_mock_herois) == 130
    sanitizer = CloudDLPSanitizer(dlp_client_adapter=fake_dlp)
    
    for heroi_data in dataset_mock_herois:
        conteudo_bruto = heroi_data["biografia"]
        sigilos = heroi_data.get("dados_sigilosos", {})
        for k, v in sigilos.items():
            conteudo_bruto += f" {k}: {v}"
            
        doc_bruto = DocumentoBruto(
            documento_id=heroi_data["id"],
            titulo=f"Ficha {heroi_data['nome_heroi']}",
            conteudo_bruto=conteudo_bruto
        )
        
        doc_sanitizado = sanitizer.sanitizar(doc_bruto)
        assert doc_sanitizado.documento_id == heroi_data["id"]
        # Garante que nenhum SSN vazou sem mascaramento
        if "documento_pii_ssn" in sigilos:
            assert sigilos["documento_pii_ssn"] not in doc_sanitizado.conteudo_sanitizado
