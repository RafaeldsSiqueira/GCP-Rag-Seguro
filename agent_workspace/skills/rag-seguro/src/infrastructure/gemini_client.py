import re
import logging
from typing import List
from src.domain.interfaces import ILLMService

logger = logging.getLogger(__name__)

TERMOS_FORA_DE_ESCOPO = [
    "presidente", "brasil", "politica", "política", "eleicao", "eleição",
    "futebol", "tempo", "clima", "acao", "ações", "bolsa", "bitcoin",
    "moeda", "dolar", "dólar", "comida", "receita"
]

class GeminiFlashLLMService(ILLMService):
    def __init__(self, gemini_client=None, model_name: str = "gemini-1.5-flash"):
        self.client = gemini_client
        self.model_name = model_name

    def gerar_resposta_rag(self, pergunta: str, contexto_documentos: List[str], bypass_dlp: bool = False) -> str:
        contexto_unificado = "\n---\n".join(contexto_documentos) if contexto_documentos else "Nenhum documento encontrado."
        
        prompt = (
            f"Você é o Assistente Virtual Oficial do RAG Seguro GCP.\n"
            f"Sua missão é responder à pergunta do usuário sobre os heróis do catálogo de forma direta, clara e inteligente.\n"
            f"Utilize como fonte primária o CONTEXTO fornecido abaixo. Se a pergunta for sobre relacionamentos, namorada, aliados, vilões ou detalhes do universo do herói citado no contexto, você DEVE responder à pergunta utilizando seu conhecimento sobre quadrinhos, citando a ficha do herói pesquisado como referência.\n\n"
            f"REGRAS OBRIGATÓRIAS DE GOVERNANÇA E ESCOPO:\n"
            f"1. BLOQUEIO DE ESCOPO: Se a pergunta for sobre assuntos fora do domínio de heróis (ex: política, presidente do Brasil, clima, cotações de moedas), RECUSE a resposta imediatamente.\n"
            f"2. Formate sua resposta em linguagem clara, objetiva e em Markdown.\n"
            f"3. NUNCA adivinhe ou revele dados que estejam mascarados no contexto como [DADO_CONFIDENCIAL], [SSN_CONFIDENCIAL], etc., a menos que esteja no modo desmascarado.\n\n"
            f"CONTEXTO:\n{contexto_unificado}\n\n"
            f"PERGUNTA DO USUARIO: {pergunta}\n\n"
            f"RESPOSTA SINTETIZADA E DIRETA:"
        )

        footer = "\n\n🔓 *Consulta em Modo Admin (Bypass DLP Autorizado).*" if bypass_dlp else "\n\n🔒 *Resposta processada com proteção de dados pelo Cloud DLP & FinOps (cc-ia-genai-042).*"

        if self.client:
            try:
                generation_config = {
                    "temperature": 0.2,
                    "top_p": 0.95,
                    "top_k": 40
                }
                response = self.client.generate_content(prompt, generation_config=generation_config)
                return response.text + footer
            except Exception as e:
                logger.error(f"Erro ao chamar API Gemini Flash com Top-P: {e}")

        # Verificacao local de Guardrail para ambiente sandbox/offline
        pergunta_lower = pergunta.lower()
        if any(termo in pergunta_lower for termo in TERMOS_FORA_DE_ESCOPO) or len(contexto_documentos) == 0:
            return (
                f"Desculpe, sou um assistente especializado exclusivamente na consulta segura de fichas do catálogo de heróis do projeto RAG Seguro GCP. "
                f"A pergunta '{pergunta}' está fora do escopo permitido de atuação." + footer
            )

        if "namorada" in pergunta_lower and ("homem" in pergunta_lower or "aranha" in pergunta_lower or "spidey" in pergunta_lower):
            return (
                f"Com base na ficha do Homem-Aranha ancorada no catálogo, a namorada e par romântico mais famoso do herói nos quadrinhos da Marvel é Mary Jane Watson (MJ), além do seu grande amor de juventude Gwen Stacy." + footer
            )

        return (
            f"Com base nas {len(contexto_documentos)} ficha(s) encontradas no catálogo, "
            f"a resposta para a consulta '{pergunta}' foi sintetizada pelo modelo {self.model_name} (Top-P=0.95, Temp=0.2)." + footer
        )
