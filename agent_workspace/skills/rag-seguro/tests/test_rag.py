from src.domain.entities import DocumentoBruto, VetorDocumento
from src.use_cases.ingestar_documento import IngestarDocumentoUseCase
from src.use_cases.consultar_rag import ConsultarRAGUseCase

def test_ingestar_documento_com_sanitizacao_e_embedding(fake_dlp, fake_vector_repo):
    doc_bruto = DocumentoBruto(
        documento_id="batman-01",
        titulo="Ficha Batman",
        conteudo_bruto="Bruce Wayne mora em Gotham e sua base é a Batcaverna"
    )
    
    use_case = IngestarDocumentoUseCase(
        sanitizer=fake_dlp,
        vector_repo=fake_vector_repo
    )
    
    resultado = use_case.executar(doc_bruto)
    
    assert resultado.documento_id == "batman-01"
    assert "[DADO_CONFIDENCIAL]" in resultado.conteudo_sanitizado
    assert len(resultado.embedding) == 768

def test_consultar_rag_com_contexto_sanitizado(fake_dlp, fake_vector_repo, fake_gemini):
    # Insere um vetor fake no repositório
    vetor_doc = VetorDocumento(
        documento_id="batman-01",
        conteudo_sanitizado="[DADO_CONFIDENCIAL] mora em [DADO_CONFIDENCIAL]",
        embedding=fake_vector_repo.gerar_embedding("onde fica a base do batman")
    )
    fake_vector_repo.salvar_vetor(vetor_doc)
    
    use_case = ConsultarRAGUseCase(
        sanitizer=fake_dlp,
        vector_repo=fake_vector_repo,
        llm_service=fake_gemini
    )
    
    resposta = use_case.executar(pergunta="Onde fica a base do Batman?", top_k=1)
    
    assert resposta.pergunta == "Onde fica a base do Batman?"
    assert "gemini-1.5-flash" in resposta.resposta_gerada
    assert len(resposta.documentos_relacionados) == 1
