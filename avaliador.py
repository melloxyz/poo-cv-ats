from gemini_api import GeminiClient
from typing import Dict, Any, Optional
import json
import re

class Avaliador:
    # Classe responsável pela avaliação de currículos usando IA
    
    def __init__(self):
        """Inicializa o avaliador com cliente Gemini"""
        try:
            self.gemini_client = GeminiClient()
            self.status_conexao = "Conectado"
        except Exception as e:
            self.gemini_client = None
            self.status_conexao = f"Erro de conexão: {str(e)}"
    
    def avaliar_curriculo(self, texto_curriculo: str, requisitos_vaga: str) -> Dict[str, Any]:
        # Avalia um currículo contra os requisitos da vaga
        if not self.gemini_client:
            return self._criar_resultado_erro("Cliente Gemini não inicializado")
        
        # Validação de entrada
        if not texto_curriculo or not texto_curriculo.strip():
            return self._criar_resultado_erro("Texto do currículo está vazio")
        
        if not requisitos_vaga or not requisitos_vaga.strip():
            return self._criar_resultado_erro("Requisitos da vaga não foram fornecidos")
        
        # Pré-processamento do texto
        texto_processado = self._preprocessar_texto(texto_curriculo)
        requisitos_processados = self._preprocessar_texto(requisitos_vaga)
        
        try:
            # Chama o Gemini para avaliação
            resultado_bruto = self.gemini_client.avaliar_curriculo(
                texto_processado, 
                requisitos_processados
            )
            
            # Processa e valida o resultado
            resultado_processado = self._processar_resultado(resultado_bruto)
            
            return resultado_processado
            
        except Exception as e:
            return self._criar_resultado_erro(f"Erro durante avaliação: {str(e)}")
    
    def _preprocessar_texto(self, texto: str) -> str:
        # Pré-processa o texto removendo caracteres especiais
        # Remove quebras de linha excessivas
        texto = re.sub(r'\n+', '\n', texto)
        
        # Remove espaços excessivos
        texto = re.sub(r'\s+', ' ', texto)
        
        # Remove caracteres especiais problemáticos
        texto = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', texto)
        
        return texto.strip()
    
    def _processar_resultado(self, resultado_bruto: Dict[str, Any]) -> Dict[str, Any]:
        # Processa e valida o resultado do Gemini
        # Verifica se houve erro na resposta
        if "erro" in resultado_bruto:
            return self._criar_resultado_erro(resultado_bruto["erro"])
        
        try:
            # Valida e ajusta o score
            score = resultado_bruto.get("score", 0)
            if not isinstance(score, (int, float)) or score < 0 or score > 100:
                score = 0
            
            # Processa pontos fortes
            pontos_fortes = resultado_bruto.get("pontos_fortes", [])
            if not isinstance(pontos_fortes, list):
                pontos_fortes = []
            pontos_fortes = [str(ponto).strip() for ponto in pontos_fortes if str(ponto).strip()]
            
            # Processa pontos fracos
            pontos_fracos = resultado_bruto.get("pontos_fracos", [])
            if not isinstance(pontos_fracos, list):
                pontos_fracos = []
            pontos_fracos = [str(ponto).strip() for ponto in pontos_fracos if str(ponto).strip()]
            
            # Processa avaliação detalhada
            avaliacao_detalhada = resultado_bruto.get("avaliacao_detalhada", "")
            if not isinstance(avaliacao_detalhada, str):
                avaliacao_detalhada = "Avaliação não disponível"
            
            # Processa informações adicionais
            nome_candidato = resultado_bruto.get("nome_candidato", "Não identificado")
            principais_habilidades = resultado_bruto.get("principais_habilidades", [])
            if not isinstance(principais_habilidades, list):
                principais_habilidades = []
            
            # Determina classificação baseada no score
            classificacao = self._obter_classificacao_score(score)
            
            return {
                "sucesso": True,
                "score": int(score),
                "classificacao": classificacao,
                "pontos_fortes": pontos_fortes[:5],  # Limita a 5 pontos
                "pontos_fracos": pontos_fracos[:5],  # Limita a 5 pontos
                "avaliacao_detalhada": avaliacao_detalhada,
                "nome_candidato": nome_candidato,
                "principais_habilidades": principais_habilidades[:10],  # Limita a 10 habilidades
                "resumo": self._gerar_resumo_avaliacao(score, pontos_fortes, pontos_fracos)
            }
            
        except Exception as e:
            return self._criar_resultado_erro(f"Erro ao processar resultado: {str(e)}")
    
    def _obter_classificacao_score(self, score: float) -> str:
        # Obtém classificação textual baseada no score
        if score >= 90:
            return "Excelente"
        elif score >= 80:
            return "Muito Bom"
        elif score >= 70:
            return "Bom"
        elif score >= 60:
            return "Regular"
        elif score >= 50:
            return "Abaixo da Média"
        else:
            return "Inadequado"
    
    def _gerar_resumo_avaliacao(self, score: int, pontos_fortes: list, pontos_fracos: list) -> str:
        # Gera um resumo breve da avaliação
        classificacao = self._obter_classificacao_score(score)
        
        resumo = f"Candidato com classificação {classificacao} ({score}/100). "
        
        if pontos_fortes:
            resumo += f"Principais qualificações: {', '.join(pontos_fortes[:2])}. "
        
        if pontos_fracos:
            resumo += f"Principais lacunas: {', '.join(pontos_fracos[:2])}."
        
        return resumo
    
    def _criar_resultado_erro(self, mensagem_erro: str) -> Dict[str, Any]:
        # Cria um resultado de erro padronizado
        return {
            "sucesso": False,
            "erro": mensagem_erro,
            "score": 0,
            "classificacao": "Erro",
            "pontos_fortes": [],
            "pontos_fracos": [],
            "avaliacao_detalhada": f"Não foi possível processar a avaliação: {mensagem_erro}",
            "nome_candidato": "Não identificado",
            "principais_habilidades": [],
            "resumo": f"Erro na avaliação: {mensagem_erro}"
        }
    
    def verificar_status_conexao(self) -> Dict[str, Any]:
        # Verifica o status da conexão com o Gemini
        return {
            "status": self.status_conexao,
            "gemini_disponivel": self.gemini_client is not None
        }
    
    def obter_estatisticas_avaliacao(self, resultados_historicos: list) -> Dict[str, Any]:
        # Gera estatísticas básicas a partir de avaliações históricas
        if not resultados_historicos:
            return {"erro": "Nenhuma avaliação disponível"}
        
        scores = [r.get("score", 0) for r in resultados_historicos if r.get("sucesso")]
        
        if not scores:
            return {"erro": "Nenhuma avaliação válida encontrada"}
        
        return {
            "total_avaliacoes": len(scores),
            "score_medio": round(sum(scores) / len(scores), 1),
            "score_maximo": max(scores),
            "score_minimo": min(scores),
            "acima_70": len([s for s in scores if s >= 70]),
            "percentual_aprovacao": round((len([s for s in scores if s >= 70]) / len(scores)) * 100, 1)
        }