from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class DocumentoBruto:
    documento_id: str
    titulo: str
    conteudo_bruto: str

@dataclass
class DocumentoSanitizado:
    documento_id: str
    titulo: str
    conteudo_sanitizado: str
    pii_detectadas: List[str] = field(default_factory=list)
    cost_center: str = "cc-ia-genai-042"

@dataclass
class VetorDocumento:
    documento_id: str
    conteudo_sanitizado: str
    embedding: List[float]
    metadata: Dict[str, Any] = field(default_factory=dict)
    score: float = 0.85

@dataclass
class ResultadoConsultaRAG:
    pergunta: str
    resposta_gerada: str
    documentos_relacionados: List[Dict[str, Any]]
    status: str = "success"
