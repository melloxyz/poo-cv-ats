import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import json

class GeminiClient:
    """Cliente para integração com a API Gemini"""
    
    def __init__(self):
        """Inicializa o cliente Gemini carregando a chave da API"""
        load_dotenv()
        api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            raise ValueError("GEMINI_API_KEY não encontrada no arquivo .env")
        
        self.client = genai.Client(api_key=api_key)
    
    def avaliar_curriculo(self, texto_curriculo, requisitos_vaga):
        # Avalia um currículo contra os requisitos da vaga
        try:
            prompt = self._construir_prompt(texto_curriculo, requisitos_vaga)
            
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-exp", # MAIS BARATO, DEIXA ASSIM, FUNCIONA IGUAL
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3,
                    top_p=0.8,
                    top_k=40,
                    max_output_tokens=2048
                )
            )
            
            # Verifica se a resposta existe
            if not response or not response.text:
                raise ValueError("Resposta vazia da API Gemini")
            
            # Extrai apenas o JSON da resposta
            response_text = response.text.strip()
            
            # Se a resposta contém markdown, extrai o JSON
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()
            elif "```" in response_text:
                json_start = response_text.find("```") + 3
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()
            
            # Parse da resposta JSON
            try:
                resultado = json.loads(response_text)
                return resultado
            except json.JSONDecodeError:
                # Se falhar, tenta extrair JSON usando regex
                import re
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    resultado = json.loads(json_match.group())
                    return resultado
                else:
                    raise ValueError(f"Não foi possível extrair JSON válido da resposta: {response_text[:200]}...")
            
        except Exception as e:
            # Em caso de erro, retorna avaliação básica baseada em palavras-chave
            return self._avaliar_basico_fallback(texto_curriculo, requisitos_vaga, str(e))
    
    def _avaliar_basico_fallback(self, curriculo, requisitos, erro_original):
        """
        Avaliação básica de fallback quando a API Gemini falha.
        
        Args:
            curriculo (str): Texto do currículo
            requisitos (str): Requisitos da vaga
            erro_original (str): Erro que causou o fallback
            
        Returns:
            dict: Avaliação básica
        """
        import re
        
        # Extrai nome do candidato
        linhas = curriculo.split('\n')
        nome_candidato = "Não identificado"
        for linha in linhas[:3]:
            linha = linha.strip()
            if linha and len(linha) > 5 and not re.search(r'@|tel|cel|phone|email', linha.lower()):
                if not any(char.isdigit() for char in linha[:10]):
                    nome_candidato = linha
                    break
        
        # Extrai email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, curriculo)
        email_candidato = emails[0] if emails else "Não identificado"
        
        # Extrai telefone
        telefone_pattern = r'(\(?\d{2}\)?[\s-]?\d{4,5}[\s-]?\d{4})'
        telefones = re.findall(telefone_pattern, curriculo)
        telefone_candidato = telefones[0] if telefones else "Não identificado"
        
        # Análise básica de palavras-chave
        curriculo_lower = curriculo.lower()
        requisitos_lower = requisitos.lower()
        
        # Tecnologias comuns
        tecnologias = ['python', 'javascript', 'java', 'sql', 'html', 'css', 'react', 'angular', 'node']
        habilidades_encontradas = [tech for tech in tecnologias if tech in curriculo_lower]
        
        # Score básico baseado em correspondência de palavras
        palavras_req = set(requisitos_lower.split())
        palavras_cur = set(curriculo_lower.split())
        correspondencias = len(palavras_req.intersection(palavras_cur))
        score_basico = min(85, max(25, (correspondencias / len(palavras_req)) * 100))
        
        return {
            "score": int(score_basico),
            "pontos_fortes": [
                "Experiência profissional demonstrada",
                "Qualificações técnicas relevantes", 
                "Perfil adequado ao mercado"
            ],
            "pontos_fracos": [
                "Análise limitada devido a falha na API",
                "Recomenda-se revisão manual detalhada"
            ],
            "avaliacao_detalhada": f"Avaliação básica realizada devido a falha na API Gemini: {erro_original}. O candidato apresenta qualificações básicas para a posição, mas recomenda-se uma análise manual mais detalhada para uma avaliação completa.",
            "nome_candidato": nome_candidato,
            "principais_habilidades": habilidades_encontradas[:5],
            "email_candidato": email_candidato,
            "telefone_candidato": telefone_candidato,
            "experiencia_anos": "Não identificado",
            "nivel_senioridade": "A definir",
            "aviso_fallback": True
        }
    
    def _construir_prompt(self, curriculo, requisitos):
        """
        Constrói o prompt avançado para análise detalhada de currículo.
        
        Args:
            curriculo (str): Texto do currículo
            requisitos (str): Requisitos da vaga
            
        Returns:
            str: Prompt formatado para o Gemini com análise granular
        """
        
        # Análise prévia dos requisitos para melhorar a avaliação
        requisitos_estruturados = self._estruturar_requisitos(requisitos)
        
        prompt = f"""
Você é um Head de Recrutamento Senior com 20 anos de experiência em seleção técnica e comportamental. 
Execute uma análise EXTREMAMENTE CRITERIOSA e PRECISA do currículo contra os requisitos específicos da vaga.

CURRÍCULO DO CANDIDATO:
{curriculo[:4000]}

REQUISITOS DA VAGA ESTRUTURADOS:
{requisitos_estruturados}

METODOLOGIA DE AVALIAÇÃO AVANÇADA:

1. ANÁLISE TÉCNICA GRANULAR (40% do score):
   - Compare cada tecnologia/ferramenta específica mencionada nos requisitos
   - Verifique nível de experiência: iniciante (1-2 anos), pleno (3-5 anos), senior (5+ anos)
   - Analise projetos que demonstrem o uso dessas tecnologias
   - Considere certificações e cursos relevantes

2. ANÁLISE DE EXPERIÊNCIA (30% do score):
   - Tempo total de experiência na área
   - Relevância das empresas/projetos anteriores
   - Progressão de carreira e responsabilidades
   - Aderência ao nível hierárquico solicitado

3. ANÁLISE DE FORMAÇÃO (20% do score):
   - Curso superior relacionado à área
   - Pós-graduação, MBA ou especializações
   - Cursos técnicos e certificações
   - Educação continuada

4. ANÁLISE COMPORTAMENTAL (10% do score):
   - Soft skills demonstradas
   - Liderança e trabalho em equipe
   - Capacidade de comunicação
   - Adaptabilidade e aprendizado

CRITÉRIOS DE PONTUAÇÃO RIGOROSA:
- 90-100: Candidato EXCEPCIONAL - Supera todos os requisitos
- 80-89: Candidato MUITO BOM - Atende plenamente os requisitos
- 70-79: Candidato BOM - Atende a maioria dos requisitos
- 60-69: Candidato REGULAR - Atende requisitos básicos
- 50-59: Candidato INADEQUADO - Não atende requisitos essenciais
- 0-49: Candidato REJEITADO - Perfil incompatível

INSTRUÇÕES CRÍTICAS:
- Seja RIGOROSO na avaliação - pontuações altas devem ser justificadas
- Compare EXATAMENTE com o que foi pedido nos requisitos
- Identifique gaps específicos e impactos na performance
- Forneça feedback ACIONÁVEL para o candidato
- Use dados quantitativos quando possível (anos de experiência, projetos, etc.)

FORMATO DE RESPOSTA OBRIGATÓRIO (JSON PURO):
{{
    "score": 75,
    "score_detalhado": {{
        "tecnico": 78,
        "experiencia": 82,
        "formacao": 65,
        "comportamental": 70
    }},
    "pontos_fortes": [
        "8+ anos experiência em Python com foco em ML",
        "Liderou equipe de 5 desenvolvedores por 3 anos",
        "Especialização em AWS e arquitetura de microserviços",
        "Histórico comprovado de entrega de projetos complexos"
    ],
    "pontos_fracos": [
        "Sem experiência em Kubernetes (requisito essencial)",
        "Falta formação em Ciência de Dados",
        "Não demonstra conhecimento em metodologias ágeis",
        "Ausência de certificações cloud"
    ],
    "avaliacao_detalhada": "ANÁLISE TÉCNICA: O candidato apresenta sólida experiência em Python (8 anos) e demonstra conhecimento avançado em machine learning através de 3 projetos documentados. Possui experiência com AWS (4 anos) e arquitetura de microserviços. LACUNAS CRÍTICAS: Não possui experiência em Kubernetes, que é requisito obrigatório para a posição. EXPERIÊNCIA: Progressão consistente de júnior a líder técnico, com gestão de equipes. FORMAÇÃO: Graduação em Engenharia, mas falta especialização em Data Science. RECOMENDAÇÃO: Candidato com potencial, mas requer capacitação em Kubernetes antes da contratação.",
    "nome_candidato": "João Silva Santos",
    "principais_habilidades": [
        "Python (8 anos)",
        "Machine Learning (5 anos)", 
        "AWS (4 anos)",
        "Liderança técnica (3 anos)",
        "Microserviços (2 anos)"
    ],
    "email_candidato": "joao.silva@email.com",
    "telefone_candidato": "(11) 99999-9999",
    "experiencia_anos": 8,
    "nivel_senioridade": "Senior",
    "recomendacao_contratacao": "Condicional - Requer treinamento em Kubernetes",
    "compatibilidade_vaga": 75,
    "risk_assessment": "Médio - Lacunas técnicas específicas identificadas",
    "proximos_passos": [
        "Entrevista técnica focada em arquitetura de sistemas",
        "Teste prático de Kubernetes",
        "Validação de experiência em liderança"
    ]
}}

RESPONDA EXCLUSIVAMENTE EM JSON VÁLIDO, SEM TEXTO ADICIONAL."""
        
        return prompt
    
    def _estruturar_requisitos(self, requisitos):
        """
        Estrutura os requisitos da vaga para melhor análise pela IA.
        
        Args:
            requisitos (str): Texto dos requisitos
            
        Returns:
            str: Requisitos estruturados
        """
        return f"""
REQUISITOS ORIGINAIS:
{requisitos}

CATEGORIZAÇÃO AUTOMÁTICA PARA ANÁLISE:
• TECNOLOGIAS: Identifique linguagens, frameworks, ferramentas específicas
• EXPERIÊNCIA: Anos mínimos, tipo de projetos, senioridade
• FORMAÇÃO: Graduação, especializações, certificações
• SOFT SKILLS: Competências comportamentais mencionadas
• RESPONSABILIDADES: Atividades e entregas esperadas

PESO DOS CRITÉRIOS:
• Requisitos marcados como "obrigatório/essencial" = peso 3
• Requisitos marcados como "desejável" = peso 2  
• Requisitos não especificados = peso 1
"""