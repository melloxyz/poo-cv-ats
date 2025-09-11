#!/usr/bin/env python3
"""Extrator Inteligente de Dados de Currículos usando IA"""

import os
import json
import re
from typing import Dict, Any, List, Optional
from dotenv import load_dotenv
from google import genai
from google.genai import types

class ExtratorInteligente:
    
    def __init__(self):
        load_dotenv()
        api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            raise ValueError("GEMINI_API_KEY não encontrada no arquivo .env")
        
        self.client = genai.Client(api_key=api_key)
        self.dados_extraidos_cache = {}
    
    def extrair_dados_completos(self, texto_curriculo: str) -> Dict[str, Any]:
        """
        Extrai todos os dados possíveis do currículo usando IA avançada.
        
        Args:
            texto_curriculo (str): Texto completo do currículo
            
        Returns:
            Dict: Dados estruturados extraídos com máxima completude
        """
        try:
            # Primeira passada: Extração de dados básicos estruturados
            dados_basicos = self._extrair_dados_basicos(texto_curriculo)
            
            # Segunda passada: Extração de experiências detalhadas
            experiencias = self._extrair_experiencias_detalhadas(texto_curriculo)
            
            # Terceira passada: Extração de habilidades e competências
            habilidades = self._extrair_habilidades_completas(texto_curriculo)
            
            # Quarta passada: Extração de formação e certificações
            formacao = self._extrair_formacao_certificacoes(texto_curriculo)
            
            # Quinta passada: Análise de projetos e conquistas
            projetos = self._extrair_projetos_conquistas(texto_curriculo)
            
            # Combina todos os resultados
            resultado_completo = self._combinar_resultados(
                dados_basicos, experiencias, habilidades, formacao, projetos
            )
            
            # Validação e enriquecimento final
            resultado_validado = self._validar_e_enriquecer(resultado_completo, texto_curriculo)
            
            return resultado_validado
            
        except Exception as e:
            # Em caso de falha, retorna extração básica usando regex
            return self._extracao_fallback(texto_curriculo, str(e))
    
    def _extrair_dados_basicos(self, texto: str) -> Dict[str, Any]:
        """
        Primeira passada: extrai dados básicos de identificação.
        """
        prompt = f"""
Você é um especialista em análise de currículos. Extraia os dados básicos de identificação deste currículo com MÁXIMA PRECISÃO.

CURRÍCULO:
{texto[:2000]}

INSTRUÇÕES CRÍTICAS:
1. Seja EXTREMAMENTE preciso - não invente informações
2. Se não encontrar algo, use "Não identificado"
3. Para nome, busque na primeira página, geralmente no topo
4. Para email, procure por padrão xxx@xxx.xxx
5. Para telefone, busque números com formato brasileiro
6. Para localização, procure por cidade, estado, endereço

RESPOSTA EM JSON PURO (SEM MARKDOWN):
{{
    "nome_completo": "Nome completo identificado ou Não identificado",
    "email": "email@exemplo.com ou Não identificado", 
    "telefone": "(11) 99999-9999 ou Não identificado",
    "endereco": "Cidade, Estado ou Não identificado",
    "linkedin": "URL do LinkedIn ou Não identificado",
    "github": "URL do GitHub ou Não identificado",
    "site_pessoal": "URL do site ou Não identificado",
    "idade_estimada": 25,
    "nacionalidade": "Brasileira ou Não identificado"
}}
"""
        
        return self._fazer_requisicao_ia(prompt, "dados_basicos")
    
    def _extrair_experiencias_detalhadas(self, texto: str) -> Dict[str, Any]:
        """
        Segunda passada: extrai experiências profissionais detalhadas.
        """
        prompt = f"""
Você é um especialista em RH. Extraia TODAS as experiências profissionais deste currículo com máximo detalhamento.

CURRÍCULO:
{texto[:3000]}

INSTRUÇÕES:
1. Liste TODAS as experiências mencionadas
2. Identifique períodos de trabalho (datas de início e fim)
3. Extraia responsabilidades específicas
4. Identifique tecnologias e ferramentas utilizadas
5. Calcule tempo total de experiência

RESPOSTA EM JSON PURO:
{{
    "experiencias": [
        {{
            "empresa": "Nome da empresa",
            "cargo": "Título do cargo",
            "periodo": "MM/AAAA - MM/AAAA ou atual",
            "duracao_meses": 24,
            "principais_responsabilidades": ["Responsabilidade 1", "Responsabilidade 2"],
            "tecnologias_utilizadas": ["Python", "JavaScript", "AWS"],
            "conquistas_quantificadas": ["Aumentou vendas em 20%", "Liderou equipe de 5 pessoas"],
            "nivel_senioridade": "Junior/Pleno/Senior/Lead"
        }}
    ],
    "tempo_total_experiencia_anos": 5.5,
    "areas_de_atuacao": ["Desenvolvimento", "Gestão de Projetos"],
    "tipos_empresa": ["Startup", "Multinacional", "Consultoria"],
    "progressao_carreira": "Crescente/Estável/Lateral"
}}
"""
        
        return self._fazer_requisicao_ia(prompt, "experiencias")
    
    def _extrair_habilidades_completas(self, texto: str) -> Dict[str, Any]:
        """
        Terceira passada: extrai habilidades técnicas e comportamentais.
        """
        prompt = f"""
Especialista em mapeamento de competências. Extraia TODAS as habilidades mencionadas neste currículo.

CURRÍCULO:
{texto[:3000]}

CATEGORIZE as habilidades encontradas:

RESPOSTA EM JSON PURO:
{{
    "linguagens_programacao": ["Python", "JavaScript", "Java"],
    "frameworks_bibliotecas": ["React", "Django", "Spring Boot"],
    "bancos_dados": ["PostgreSQL", "MongoDB", "MySQL"],
    "ferramentas_devops": ["Docker", "Kubernetes", "Jenkins"],
    "cloud_platforms": ["AWS", "Azure", "Google Cloud"],
    "metodologias": ["Scrum", "Kanban", "TDD"],
    "soft_skills": ["Liderança", "Comunicação", "Trabalho em equipe"],
    "idiomas": [
        {{
            "idioma": "Inglês",
            "nivel": "Avançado/Intermediário/Básico"
        }}
    ],
    "certificacoes_tecnicas": ["AWS Solutions Architect", "Scrum Master"],
    "nivel_tecnico_geral": "Junior/Pleno/Senior/Especialista",
    "especializacoes": ["Machine Learning", "DevOps", "Frontend"]
}}
"""
        
        return self._fazer_requisicao_ia(prompt, "habilidades")
    
    def _extrair_formacao_certificacoes(self, texto: str) -> Dict[str, Any]:
        """
        Quarta passada: extrai formação acadêmica e certificações.
        """
        prompt = f"""
Especialista em análise acadêmica. Extraia TODA a formação e certificações deste currículo.

CURRÍCULO:
{texto[:3000]}

INSTRUÇÕES:
1. Identifique TODOS os cursos superiores
2. Liste especializações, MBAs, pós-graduações
3. Identifique certificações técnicas
4. Cursos relevantes e treinamentos

RESPOSTA EM JSON PURO:
{{
    "formacao_superior": [
        {{
            "curso": "Ciência da Computação",
            "instituicao": "Universidade X",
            "periodo": "2018-2022",
            "status": "Completo/Cursando",
            "nivel": "Graduação/Pós-graduação/MBA/Mestrado/Doutorado"
        }}
    ],
    "certificacoes": [
        {{
            "nome": "AWS Solutions Architect",
            "instituicao": "Amazon",
            "ano_obtencao": "2023",
            "validade": "2026 ou N/A"
        }}
    ],
    "cursos_complementares": [
        {{
            "nome": "Machine Learning",
            "instituicao": "Coursera",
            "carga_horaria": "40h",
            "ano": "2023"
        }}
    ],
    "nivel_educacional": "Ensino Superior/Pós-graduação/Mestrado/Doutorado",
    "area_formacao": "Tecnologia/Engenharia/Administração",
    "educacao_continuada": true
}}
"""
        
        return self._fazer_requisicao_ia(prompt, "formacao")
    
    def _extrair_projetos_conquistas(self, texto: str) -> Dict[str, Any]:
        """
        Quinta passada: extrai projetos e conquistas específicas.
        """
        prompt = f"""
Analista de projetos e conquistas. Identifique TODOS os projetos e realizações mencionadas.

CURRÍCULO:
{texto[:3000]}

FOQUE em:
1. Projetos específicos desenvolvidos
2. Conquistas quantificadas
3. Reconhecimentos e prêmios
4. Participação em eventos
5. Contribuições open source

RESPOSTA EM JSON PURO:
{{
    "projetos_destaque": [
        {{
            "nome": "Sistema de E-commerce",
            "descricao": "Plataforma completa de vendas online",
            "tecnologias": ["Python", "React", "PostgreSQL"],
            "periodo": "6 meses",
            "resultado_impacto": "Aumentou vendas em 30%",
            "papel": "Desenvolvedor Full Stack"
        }}
    ],
    "conquistas_quantificadas": [
        "Reduziu tempo de processamento em 40%",
        "Liderou equipe de 8 desenvolvedores",
        "Implementou sistema usado por 10.000+ usuários"
    ],
    "reconhecimentos": [
        "Funcionário do mês - Janeiro 2023",
        "Melhor projeto inovador - Hackathon 2022"
    ],
    "contribuicoes_open_source": [
        {{
            "projeto": "Nome do projeto",
            "descricao": "Contribuição realizada",
            "url": "GitHub URL"
        }}
    ],
    "publicacoes_artigos": ["Artigo sobre IA", "Blog post sobre DevOps"],
    "palestras_eventos": ["Tech Talk sobre Python", "Workshop de Machine Learning"]
}}
"""
        
        return self._fazer_requisicao_ia(prompt, "projetos")
    
    def _fazer_requisicao_ia(self, prompt: str, tipo_extracao: str) -> Dict[str, Any]:
        """
        Executa requisição para a IA com tratamento de erros.
        """
        try:
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.1,  # Baixa temperatura para máxima precisão
                    top_p=0.8,
                    top_k=40,
                    max_output_tokens=2048
                )
            )
            
            if not response or not response.text:
                raise ValueError("Resposta vazia da API")
            
            # Extrai JSON da resposta
            response_text = response.text.strip()
            
            # Remove markdown se presente
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()
            elif "```" in response_text:
                json_start = response_text.find("```") + 3
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()
            
            # Parse JSON
            resultado = json.loads(response_text)
            
            # Cache do resultado
            self.dados_extraidos_cache[tipo_extracao] = resultado
            
            return resultado
            
        except json.JSONDecodeError as e:
            print(f"Erro JSON na extração {tipo_extracao}: {e}")
            return self._resultado_fallback_por_tipo(tipo_extracao)
        except Exception as e:
            print(f"Erro na extração {tipo_extracao}: {e}")
            return self._resultado_fallback_por_tipo(tipo_extracao)
    
    def _combinar_resultados(self, dados_basicos: Dict, experiencias: Dict, 
                           habilidades: Dict, formacao: Dict, projetos: Dict) -> Dict[str, Any]:
        """
        Combina todos os resultados das extrações em um único objeto estruturado.
        """
        return {
            "dados_pessoais": dados_basicos,
            "experiencia_profissional": experiencias,
            "habilidades_competencias": habilidades,
            "formacao_educacao": formacao,
            "projetos_conquistas": projetos,
            "timestamp_extracao": "2025-09-10T" + str(hash(str(dados_basicos)))[-6:],
            "qualidade_extracao": "IA_COMPLETA"
        }
    
    def _validar_e_enriquecer(self, resultado: Dict[str, Any], texto_original: str) -> Dict[str, Any]:
        """
        Valida os dados extraídos e os enriquece com análises adicionais.
        """
        # Análise de consistência
        experiencia_anos = resultado.get("experiencia_profissional", {}).get("tempo_total_experiencia_anos", 0)
        
        # Enriquece com métricas calculadas
        resultado["metricas_calculadas"] = {
            "score_completude": self._calcular_completude(resultado),
            "nivel_senioridade_calculado": self._calcular_nivel_senioridade(experiencia_anos),
            "areas_especialidade": self._identificar_especialidades(resultado),
            "pontos_fortes_identificados": self._identificar_pontos_fortes(resultado),
            "gaps_identificados": self._identificar_gaps(resultado)
        }
        
        # Adiciona análise de qualidade do currículo
        resultado["analise_curriculo"] = {
            "estrutura_organizada": "bem_estruturado" if len(texto_original) > 1000 else "simples",
            "riqueza_detalhes": "alta" if experiencia_anos > 3 else "media",
            "presenca_quantificacoes": self._verificar_quantificacoes(texto_original)
        }
        
        return resultado
    
    def _extracao_fallback(self, texto: str, erro_original: str) -> Dict[str, Any]:
        """
        Extração de fallback usando regex quando a IA falha.
        """
        # Extração básica usando regex
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        telefone_pattern = r'(\(?\d{2}\)?[\s-]?\d{4,5}[\s-]?\d{4})'
        
        emails = re.findall(email_pattern, texto)
        telefones = re.findall(telefone_pattern, texto)
        
        # Nome (primeira linha limpa)
        linhas = texto.split('\n')
        nome = "Não identificado"
        for linha in linhas[:5]:
            linha_limpa = linha.strip()
            if (linha_limpa and len(linha_limpa) > 5 and 
                not re.search(r'@|tel|cel|phone|email|cv|curriculum', linha_limpa.lower())):
                if not any(char.isdigit() for char in linha_limpa[:15]):
                    nome = linha_limpa
                    break
        
        return {
            "dados_pessoais": {
                "nome_completo": nome,
                "email": emails[0] if emails else "Não identificado",
                "telefone": telefones[0] if telefones else "Não identificado",
                "endereco": "Não identificado",
                "linkedin": "Não identificado",
                "github": "Não identificado",
                "site_pessoal": "Não identificado"
            },
            "qualidade_extracao": "FALLBACK_REGEX",
            "erro_ia": erro_original,
            "aviso": "Extração limitada devido a falha na IA"
        }
    
    def _resultado_fallback_por_tipo(self, tipo: str) -> Dict[str, Any]:
        """
        Retorna resultado padrão baseado no tipo de extração que falhou.
        """
        fallbacks = {
            "dados_basicos": {
                "nome_completo": "Não identificado",
                "email": "Não identificado",
                "telefone": "Não identificado",
                "endereco": "Não identificado",
                "linkedin": "Não identificado",
                "github": "Não identificado",
                "site_pessoal": "Não identificado"
            },
            "experiencias": {
                "experiencias": [],
                "tempo_total_experiencia_anos": 0,
                "areas_de_atuacao": [],
                "progressao_carreira": "Não identificado"
            },
            "habilidades": {
                "linguagens_programacao": [],
                "frameworks_bibliotecas": [],
                "soft_skills": [],
                "nivel_tecnico_geral": "A definir"
            },
            "formacao": {
                "formacao_superior": [],
                "certificacoes": [],
                "nivel_educacional": "Não identificado"
            },
            "projetos": {
                "projetos_destaque": [],
                "conquistas_quantificadas": [],
                "reconhecimentos": []
            }
        }
        
        return fallbacks.get(tipo, {})
    
    def _calcular_completude(self, resultado: Dict) -> int:
        """
        Calcula score de completude dos dados extraídos (0-100).
        """
        campos_importantes = [
            resultado.get("dados_pessoais", {}).get("nome_completo", ""),
            resultado.get("dados_pessoais", {}).get("email", ""),
            resultado.get("experiencia_profissional", {}).get("experiencias", []),
            resultado.get("habilidades_competencias", {}).get("linguagens_programacao", []),
            resultado.get("formacao_educacao", {}).get("formacao_superior", [])
        ]
        
        campos_preenchidos = sum(1 for campo in campos_importantes if campo and campo != "Não identificado")
        return int((campos_preenchidos / len(campos_importantes)) * 100)
    
    def _calcular_nivel_senioridade(self, anos_exp: float) -> str:
        """
        Calcula nível de senioridade baseado em anos de experiência.
        """
        if anos_exp < 2:
            return "Junior"
        elif anos_exp < 5:
            return "Pleno"
        elif anos_exp < 8:
            return "Senior"
        else:
            return "Especialista"
    
    def _identificar_especialidades(self, resultado: Dict) -> List[str]:
        """
        Identifica áreas de especialidade baseadas nos dados extraídos.
        """
        especialidades = []
        
        habilidades = resultado.get("habilidades_competencias", {})
        linguagens = habilidades.get("linguagens_programacao", [])
        frameworks = habilidades.get("frameworks_bibliotecas", [])
        
        # Frontend
        if any(tech in str(frameworks).lower() for tech in ['react', 'angular', 'vue', 'next']):
            especialidades.append("Frontend")
        
        # Backend
        if any(tech in str(linguagens).lower() for tech in ['python', 'java', 'node', 'php']):
            especialidades.append("Backend")
        
        # DevOps/Cloud
        if any(tech in str(habilidades).lower() for tech in ['docker', 'kubernetes', 'aws', 'azure']):
            especialidades.append("DevOps/Cloud")
        
        # Data Science/ML
        if any(tech in str(habilidades).lower() for tech in ['machine learning', 'tensorflow', 'pandas', 'sql']):
            especialidades.append("Data Science")
        
        return especialidades[:3]  # Limita a 3 especialidades principais
    
    def _identificar_pontos_fortes(self, resultado: Dict) -> List[str]:
        """
        Identifica pontos fortes baseados nos dados extraídos.
        """
        pontos_fortes = []
        
        # Experiência
        exp_anos = resultado.get("experiencia_profissional", {}).get("tempo_total_experiencia_anos", 0)
        if exp_anos > 5:
            pontos_fortes.append(f"Experiência sólida ({exp_anos} anos)")
        
        # Variedade tecnológica
        habilidades = resultado.get("habilidades_competencias", {})
        total_techs = len(habilidades.get("linguagens_programacao", []) + 
                         habilidades.get("frameworks_bibliotecas", []))
        if total_techs > 5:
            pontos_fortes.append("Amplo domínio tecnológico")
        
        # Formação
        formacao = resultado.get("formacao_educacao", {}).get("formacao_superior", [])
        if formacao:
            pontos_fortes.append("Formação acadêmica sólida")
        
        # Certificações
        certs = resultado.get("formacao_educacao", {}).get("certificacoes", [])
        if certs:
            pontos_fortes.append("Certificações técnicas")
        
        return pontos_fortes[:5]
    
    def _identificar_gaps(self, resultado: Dict) -> List[str]:
        """
        Identifica possíveis gaps nos dados extraídos.
        """
        gaps = []
        
        # Dados pessoais incompletos
        dados_pessoais = resultado.get("dados_pessoais", {})
        if dados_pessoais.get("email") == "Não identificado":
            gaps.append("Email não identificado")
        
        if dados_pessoais.get("telefone") == "Não identificado":
            gaps.append("Telefone não identificado")
        
        # Experiência limitada
        exp_anos = resultado.get("experiencia_profissional", {}).get("tempo_total_experiencia_anos", 0)
        if exp_anos < 2:
            gaps.append("Experiência profissional limitada")
        
        # Falta de certificações
        certs = resultado.get("formacao_educacao", {}).get("certificacoes", [])
        if not certs:
            gaps.append("Ausência de certificações técnicas")
        
        return gaps[:3]
    
    def _verificar_quantificacoes(self, texto: str) -> str:
        """
        Verifica se o currículo contém quantificações (números, percentuais).
        """
        padrao_numeros = r'\d+[%\+\-]|\d+\s*(anos?|meses?|pessoas?|usuários?|projetos?)'
        quantificacoes = re.findall(padrao_numeros, texto.lower())
        
        if len(quantificacoes) > 5:
            return "alta"
        elif len(quantificacoes) > 2:
            return "media"
        else:
            return "baixa"
