from src.domain.entities import DocumentoBruto, VetorDocumento
from src.domain.interfaces import IDLPSanitizer, IVectorRepository

class IngestarDocumentoUseCase:
    def __init__(self, sanitizer: IDLPSanitizer, vector_repo: IVectorRepository):
        self.sanitizer = sanitizer
        self.vector_repo = vector_repo

    def executar(self, documento_bruto: DocumentoBruto) -> VetorDocumento:
        # 1. Sanitiza o documento bruto via DLP
        doc_sanitizado = self.sanitizer.sanitizar(documento_bruto)
        
        # 2. Gera os vetores de embedding para o texto sanitizado
        embedding = self.vector_repo.gerar_embedding(doc_sanitizado.conteudo_sanitizado)
        
        # 3. Cria a entidade VetorDocumento preservando o conteudo original para auditoria privilegiada
        vetor_doc = VetorDocumento(
            documento_id=doc_sanitizado.documento_id,
            conteudo_sanitizado=doc_sanitizado.conteudo_sanitizado,
            embedding=embedding,
            metadata={
                "titulo": doc_sanitizado.titulo,
                "cost_center": doc_sanitizado.cost_center,
                "pii_detectadas": doc_sanitizado.pii_detectadas,
                "conteudo_bruto_original": documento_bruto.conteudo_bruto
            }
        )
        
        # 4. Salva no repositório de vetores (Firestore Vector Search)
        self.vector_repo.salvar_vetor(vetor_doc)
        
        return vetor_doc
