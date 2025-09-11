from curriculo import Curriculo
from avaliador import Avaliador
from typing import Dict, Any, Optional
import pandas as pd
from datetime import datetime

class SistemaRecrutamento:
    def __init__(self):
        self.avaliador = Avaliador()
        self.curriculo_atual = None
        self.ultima_avaliacao = None
        self.historico_avaliacoes = []
    
    def processar_curriculo(self, arquivo_upload, requisitos_vaga: str) -> Dict[str, Any]:
        try:
            # Validação inicial
            resultado_validacao = self._validar_entrada(arquivo_upload, requisitos_vaga)
            if not resultado_validacao["valido"]:
                return {
                    "sucesso": False,
                    "erro": resultado_validacao["erro"],
                    "etapa": "validacao"
                }
            
            # Criação do currículo
            self.curriculo_atual = Curriculo(arquivo_upload)
            
            validacao_arquivo = self.curriculo_atual.validar_arquivo()
            if not validacao_arquivo["valido"]:
                return {
                    "sucesso": False,
                    "erro": validacao_arquivo["erro"],
                    "etapa": "validacao_arquivo"
                }
            
            # Extração de texto
            resultado_extracao = self.curriculo_atual.extrair_texto()
            if not resultado_extracao["sucesso"]:
                return {
                    "sucesso": False,
                    "erro": f"Falha na extração: {resultado_extracao['erro']}",
                    "etapa": "extracao"
                }
            
            texto_curriculo = resultado_extracao["texto"]
            dados_estruturados = resultado_extracao.get("dados_estruturados", {})
            metodo_extracao = resultado_extracao.get("metodo_extracao", "BASICO")
            
            # 4. Pré-processamento do texto para melhor análise
            texto_preprocessado = self._preprocessar_texto(texto_curriculo)
            
            # 5. Validação da qualidade do texto extraído
            validacao_qualidade = self._validar_qualidade_texto(texto_preprocessado)
            if not validacao_qualidade["valida"]:
                return {
                    "sucesso": False,
                    "erro": f"Qualidade do texto insuficiente: {validacao_qualidade['motivo']}",
                    "etapa": "qualidade_texto"
                }
            
            # 6. Enriquecimento dos requisitos com dados estruturados
            requisitos_enriquecidos = self._enriquecer_requisitos_com_dados(
                requisitos_vaga, dados_estruturados
            )
            
            # 7. Avaliação com IA aprimorada
            resultado_avaliacao = self.avaliador.avaliar_curriculo(
                texto_preprocessado, 
                requisitos_enriquecidos
            )
            
            # 8. Validação do resultado da avaliação
            resultado_validado = self._validar_resultado_avaliacao(resultado_avaliacao)
            
            # 9. Enriquecimento do resultado com dados estruturados
            resultado_enriquecido = self._enriquecer_resultado_com_dados_estruturados(
                resultado_validado,
                dados_estruturados,
                texto_preprocessado,
                requisitos_vaga,
                arquivo_upload.name
            )
            
            # 10. Armazenar no histórico
            self.ultima_avaliacao = resultado_enriquecido
            self._adicionar_ao_historico(resultado_enriquecido, arquivo_upload.name)
            
            return {
                "sucesso": True,
                "resultado": resultado_enriquecido,
                "metadados": {
                    "timestamp": datetime.now().isoformat(),
                    "nome_arquivo": arquivo_upload.name,
                    "tamanho_arquivo": arquivo_upload.size,
                    "caracteres_extraidos": len(texto_curriculo),
                    "caracteres_processados": len(texto_preprocessado),
                    "metodo_extracao": metodo_extracao,
                    "dados_estruturados_disponiveis": bool(dados_estruturados),
                    "qualidade_extracao": dados_estruturados.get("qualidade_extracao", "N/A")
                }
            }
            
        except Exception as e:
            return {
                "sucesso": False,
                "erro": f"Erro interno no sistema: {str(e)}",
                "etapa": "sistema",
                "detalhes_tecnico": type(e).__name__
            }
    
    def _preprocessar_texto(self, texto: str) -> str:
        """Pré-processa o texto do currículo"""
        import re
        
        if not texto:
            return ""
        
        # Remove caracteres especiais desnecessários mas preserva estrutura
        texto_limpo = re.sub(r'\s+', ' ', texto)  # Normaliza espaços
        texto_limpo = re.sub(r'[^\w\s@.\-(),;:!?\n]', '', texto_limpo)  # Remove caracteres especiais
        
        # Melhora formatação para seções comuns
        texto_limpo = re.sub(r'\b(EXPERIÊNCIA|EXPERIENCE|HISTÓRICO|CARREIRA)\b', '\n\nEXPERIÊNCIA PROFISSIONAL:\n', texto_limpo, flags=re.IGNORECASE)
        texto_limpo = re.sub(r'\b(FORMAÇÃO|EDUCAÇÃO|EDUCATION|ACADEMIC)\b', '\n\nFORMAÇÃO:\n', texto_limpo, flags=re.IGNORECASE)
        texto_limpo = re.sub(r'\b(HABILIDADES|SKILLS|COMPETÊNCIAS)\b', '\n\nHABILIDADES:\n', texto_limpo, flags=re.IGNORECASE)
        texto_limpo = re.sub(r'\b(CERTIFICAÇÕES|CERTIFICATES|CURSOS)\b', '\n\nCERTIFICAÇÕES:\n', texto_limpo, flags=re.IGNORECASE)
        
        # Identifica e marca seções de contato
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        telefone_pattern = r'(\(?\d{2}\)?[\s-]?\d{4,5}[\s-]?\d{4})'
        
        if re.search(email_pattern, texto_limpo):
            texto_limpo = re.sub(email_pattern, r'\n\nCONTATO - EMAIL: \g<0>\n', texto_limpo, count=1)
        
        if re.search(telefone_pattern, texto_limpo):
            texto_limpo = re.sub(telefone_pattern, r'\n\nCONTATO - TELEFONE: \g<0>\n', texto_limpo, count=1)
        
        # Limita tamanho para otimizar custo da API
        if len(texto_limpo) > 5000:
            # Prioriza as primeiras seções (geralmente mais importantes)
            texto_limpo = texto_limpo[:4500] + "\n\n[TEXTO TRUNCADO PARA OTIMIZAÇÃO]"
        
        return texto_limpo.strip()
    
    def _validar_qualidade_texto(self, texto: str) -> Dict[str, Any]:
        """Valida se o texto tem qualidade suficiente"""
        if not texto or len(texto.strip()) < 50:
            return {
                "valida": False,
                "motivo": "Texto muito curto ou vazio (mínimo 50 caracteres)"
            }
        
        # Verifica se há pelo menos algumas palavras significativas
        palavras_significativas = len([p for p in texto.split() if len(p) > 3])
        if palavras_significativas < 10:
            return {
                "valida": False,
                "motivo": "Insuficientes palavras significativas no texto extraído"
            }
        
        # Verifica se não é só lixo de caracteres
        caracteres_alfanumericos = len([c for c in texto if c.isalnum()])
        if caracteres_alfanumericos / len(texto) < 0.5:
            return {
                "valida": False,
                "motivo": "Texto com muitos caracteres não alfanuméricos (possível erro na extração)"
            }
        
        return {
            "valida": True,
            "qualidade_score": min(100, int((palavras_significativas / 50) * 100)),
            "palavras_significativas": palavras_significativas,
            "tamanho_total": len(texto)
        }
    
    def _validar_resultado_avaliacao(self, resultado: Dict[str, Any]) -> Dict[str, Any]:
        """Valida e corrige o resultado da IA"""
        # Campos obrigatórios com valores padrão
        campos_obrigatorios = {
            "score": 0,
            "pontos_fortes": [],
            "pontos_fracos": [],
            "avaliacao_detalhada": "Avaliação não disponível",
            "nome_candidato": "Não identificado",
            "principais_habilidades": [],
            "email_candidato": "Não identificado",
            "telefone_candidato": "Não identificado",
            "experiencia_anos": "Não identificado",
            "nivel_senioridade": "A definir"
        }
        
        # Aplica valores padrão para campos faltantes
        for campo, valor_padrao in campos_obrigatorios.items():
            if campo not in resultado or resultado[campo] is None:
                resultado[campo] = valor_padrao
        
        # Validações específicas
        try:
            score = int(resultado["score"])
            resultado["score"] = max(0, min(100, score))  # Garante que está entre 0-100
        except (ValueError, TypeError):
            resultado["score"] = 0
        
        # Garantir que listas são realmente listas
        for campo_lista in ["pontos_fortes", "pontos_fracos", "principais_habilidades"]:
            if not isinstance(resultado[campo_lista], list):
                resultado[campo_lista] = []
        
        # Limita tamanho das listas para evitar spam
        resultado["pontos_fortes"] = resultado["pontos_fortes"][:8]
        resultado["pontos_fracos"] = resultado["pontos_fracos"][:8]
        resultado["principais_habilidades"] = resultado["principais_habilidades"][:10]
        
        return resultado
    
    def _validar_entrada(self, arquivo_upload, requisitos_vaga: str) -> Dict[str, Any]:
        """Valida os dados de entrada do sistema"""
        if not arquivo_upload:
            return {
                "valido": False,
                "erro": "Nenhum arquivo de currículo foi carregado"
            }
        
        if not requisitos_vaga or len(requisitos_vaga.strip()) < 20:
            return {
                "valido": False,
                "erro": "Requisitos da vaga muito curtos ou vazios (mínimo: 20 caracteres)"
            }
        
        return {
            "valido": True
        }
    
    def _enriquecer_resultado(self, resultado: Dict[str, Any], texto: str, requisitos: str, nome_arquivo: str) -> Dict[str, Any]:
        """Enriquece o resultado com análises adicionais"""
        # Adiciona metadados do arquivo
        resultado["arquivo_original"] = nome_arquivo
        resultado["timestamp_avaliacao"] = datetime.now().isoformat()
        
        # Classificação baseada no score
        score = resultado.get("score", 0)
        if score >= 90:
            resultado["classificacao"] = "Excepcional"
        elif score >= 80:
            resultado["classificacao"] = "Muito Bom"
        elif score >= 70:
            resultado["classificacao"] = "Bom"
        elif score >= 60:
            resultado["classificacao"] = "Regular"
        elif score >= 50:
            resultado["classificacao"] = "Inadequado"
        else:
            resultado["classificacao"] = "Rejeitado"
        
        # Análise de compatibilidade específica
        resultado["compatibilidade_vaga"] = self._calcular_compatibilidade(texto, requisitos)
        
        # Sugestões de melhoria baseadas no score
        resultado["sugestoes_melhoria"] = self._gerar_sugestoes_melhoria(resultado)
        
        return resultado
    
    def _calcular_compatibilidade(self, texto: str, requisitos: str) -> int:
        """Calcula compatibilidade usando palavras-chave"""
        import re
        
        texto_lower = texto.lower()
        requisitos_lower = requisitos.lower()
        
        # Tecnologias comuns para verificar
        tecnologias = [
            'python', 'javascript', 'java', 'php', 'sql', 'html', 'css',
            'react', 'angular', 'vue', 'node', 'django', 'flask', 'spring',
            'aws', 'azure', 'docker', 'kubernetes', 'git', 'linux'
        ]
        
        # Conta quantas tecnologias mencionadas nos requisitos o candidato possui
        techs_requisitos = [tech for tech in tecnologias if tech in requisitos_lower]
        techs_candidato = [tech for tech in tecnologias if tech in texto_lower]
        techs_match = [tech for tech in techs_requisitos if tech in techs_candidato]
        
        if not techs_requisitos:
            return 70  # Score médio se não há tecnologias específicas
        
        compatibilidade_tech = (len(techs_match) / len(techs_requisitos)) * 100
        
        # Ajusta baseado na presença de outras palavras-chave relevantes
        palavras_experiencia = ['anos', 'experiência', 'projeto', 'desenvolvimento', 'gestão']
        bonus_experiencia = sum(1 for palavra in palavras_experiencia if palavra in texto_lower) * 2
        
        return min(100, int(compatibilidade_tech + bonus_experiencia))
    
    def _gerar_sugestoes_melhoria(self, resultado: Dict[str, Any]) -> list:
        """Gera sugestões de melhoria"""
        sugestoes = []
        score = resultado.get("score", 0)
        
        if score < 70:
            sugestoes.extend([
                "Adicione mais detalhes sobre experiências profissionais relevantes",
                "Inclua projetos específicos que demonstrem suas habilidades",
                "Destaque certificações e cursos relacionados à vaga"
            ])
        
        if score < 80:
            sugestoes.extend([
                "Quantifique seus resultados e conquistas",
                "Use palavras-chave específicas da área de interesse",
                "Organize melhor as seções do currículo"
            ])
        
        pontos_fracos = resultado.get("pontos_fracos", [])
        if len(pontos_fracos) > 3:
            sugestoes.append("Foque em desenvolver as habilidades mencionadas como pontos fracos")
        
        return sugestoes[:5]  # Limita a 5 sugestões
    
    def _adicionar_ao_historico(self, resultado: Dict[str, Any], nome_arquivo: str):
        """Adiciona resultado ao histórico"""
        entrada_historico = {
            "timestamp": datetime.now().isoformat(),
            "nome_arquivo": nome_arquivo,
            "score": resultado.get("score", 0),
            "classificacao": resultado.get("classificacao", "N/A"),
            "nome_candidato": resultado.get("nome_candidato", "Não identificado")
        }
        
        self.historico_avaliacoes.append(entrada_historico)
        
        # Limita histórico a 100 entradas para não consumir muita memória
        if len(self.historico_avaliacoes) > 100:
            self.historico_avaliacoes = self.historico_avaliacoes[-100:]
    
    def obter_historico(self) -> pd.DataFrame:
        """Retorna histórico como DataFrame"""
        if not self.historico_avaliacoes:
            return pd.DataFrame()
        
        return pd.DataFrame(self.historico_avaliacoes)
    
    def exportar_resultado_excel(self, resultado: Dict[str, Any], nome_arquivo: str = None) -> str:
        """Exporta resultado para Excel"""
        if not nome_arquivo:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"avaliacao_curriculo_{timestamp}.xlsx"
        
        # Prepara dados para Excel
        dados_principais = {
            "Campo": ["Nome", "Score", "Classificação", "Experiência", "Nível"],
            "Valor": [
                resultado.get("nome_candidato", "N/A"),
                resultado.get("score", 0),
                resultado.get("classificacao", "N/A"),
                resultado.get("experiencia_anos", "N/A"),
                resultado.get("nivel_senioridade", "N/A")
            ]
        }
        
        with pd.ExcelWriter(nome_arquivo, engine='openpyxl') as writer:
            # Aba principal
            df_principais = pd.DataFrame(dados_principais)
            df_principais.to_excel(writer, sheet_name='Resumo', index=False)
            
            # Aba de pontos fortes
            if resultado.get("pontos_fortes"):
                df_fortes = pd.DataFrame({"Pontos Fortes": resultado["pontos_fortes"]})
                df_fortes.to_excel(writer, sheet_name='Pontos Fortes', index=False)
            
            # Aba de pontos fracos
            if resultado.get("pontos_fracos"):
                df_fracos = pd.DataFrame({"Pontos Fracos": resultado["pontos_fracos"]})
                df_fracos.to_excel(writer, sheet_name='Pontos Fracos', index=False)
        
        return nome_arquivo
    
    def obter_status_sistema(self) -> Dict[str, Any]:
        """Retorna status atual do sistema"""
        try:
            # Verifica se o avaliador está funcionando
            avaliador_ok = self.avaliador is not None
            
            # Verifica se há avaliações no histórico
            total_avaliacoes = len(self.historico_avaliacoes)
            
            # Verifica configurações básicas
            import os
            api_key_configurada = bool(os.getenv('GEMINI_API_KEY'))
            
            # Verifica se o Gemini está conectado e funcionando
            gemini_conectado = False
            try:
                if self.avaliador and hasattr(self.avaliador, 'gemini_client'):
                    # Verifica se o cliente foi inicializado corretamente
                    if self.avaliador.gemini_client is not None:
                        # Verifica se tem API key e se o status de conexão é positivo
                        if (api_key_configurada and 
                            hasattr(self.avaliador, 'status_conexao') and 
                            self.avaliador.status_conexao == "Conectado"):
                            gemini_conectado = True
                        else:
                            gemini_conectado = False
                    else:
                        gemini_conectado = False
                else:
                    gemini_conectado = False
            except Exception as e:
                print(f"Erro ao verificar conexão Gemini: {e}")
                gemini_conectado = False
            
            return {
                "sistema_ativo": True,
                "avaliador_inicializado": avaliador_ok,
                "api_key_configurada": api_key_configurada,
                "gemini_conectado": gemini_conectado,
                "total_avaliacoes_realizadas": total_avaliacoes,
                "ultima_avaliacao": self.ultima_avaliacao is not None,
                "memoria_sistema": f"{len(self.historico_avaliacoes)}/100 avaliações em cache",
                "status": "Sistema operacional e pronto para uso"
            }
            
        except Exception as e:
            return {
                "sistema_ativo": False,
                "erro": str(e),
                "status": f"Sistema com problemas: {str(e)}"
            }
    
    def _enriquecer_requisitos_com_dados(self, requisitos: str, dados_estruturados: Dict[str, Any]) -> str:
        """Enriquece requisitos com dados estruturados"""
        if not dados_estruturados or dados_estruturados.get("qualidade_extracao") == "FALHA":
            return requisitos
        
        requisitos_enriquecidos = f"""
{requisitos}

======= CONTEXTO ADICIONAL DO CANDIDATO PARA ANÁLISE =======

DADOS ESTRUTURADOS EXTRAÍDOS DO CURRÍCULO:

📋 DADOS PESSOAIS:
{self._formatar_dados_pessoais(dados_estruturados.get("dados_pessoais", {}))}

💼 EXPERIÊNCIA PROFISSIONAL:
{self._formatar_experiencia(dados_estruturados.get("experiencia_profissional", {}))}

🛠️ HABILIDADES E COMPETÊNCIAS:
{self._formatar_habilidades(dados_estruturados.get("habilidades_competencias", {}))}

🎓 FORMAÇÃO E EDUCAÇÃO:
{self._formatar_formacao(dados_estruturados.get("formacao_educacao", {}))}

🚀 PROJETOS E CONQUISTAS:
{self._formatar_projetos(dados_estruturados.get("projetos_conquistas", {}))}

📊 MÉTRICAS CALCULADAS:
{self._formatar_metricas(dados_estruturados.get("metricas_calculadas", {}))}

IMPORTANTE: Use estas informações estruturadas para uma análise mais precisa e completa!
"""
        
        return requisitos_enriquecidos
    
    def _enriquecer_resultado_com_dados_estruturados(self, resultado: Dict[str, Any], 
                                                   dados_estruturados: Dict[str, Any],
                                                   texto: str, requisitos: str, 
                                                   nome_arquivo: str) -> Dict[str, Any]:
        """
        Enriquece o resultado da avaliação com os dados estruturados extraídos.
        
        Args:
            resultado (Dict): Resultado base da avaliação
            dados_estruturados (Dict): Dados estruturados extraídos
            texto (str): Texto do currículo
            requisitos (str): Requisitos da vaga
            nome_arquivo (str): Nome do arquivo
            
        Returns:
            Dict: Resultado super enriquecido
        """
        # Usa o método original como base
        resultado_enriquecido = self._enriquecer_resultado(resultado, texto, requisitos, nome_arquivo)
        
        # Adiciona dados estruturados se disponíveis
        if dados_estruturados and dados_estruturados.get("qualidade_extracao") != "FALHA":
            
            # Sobrescreve dados básicos com informações mais precisas da IA
            dados_pessoais = dados_estruturados.get("dados_pessoais", {})
            if dados_pessoais.get("nome_completo", "") != "Não identificado":
                resultado_enriquecido["nome_candidato"] = dados_pessoais["nome_completo"]
            if dados_pessoais.get("email", "") != "Não identificado":
                resultado_enriquecido["email_candidato"] = dados_pessoais["email"]
            if dados_pessoais.get("telefone", "") != "Não identificado":
                resultado_enriquecido["telefone_candidato"] = dados_pessoais["telefone"]
            
            # Adiciona informações adicionais de contato
            resultado_enriquecido["linkedin_candidato"] = dados_pessoais.get("linkedin", "Não identificado")
            resultado_enriquecido["github_candidato"] = dados_pessoais.get("github", "Não identificado")
            resultado_enriquecido["endereco_candidato"] = dados_pessoais.get("endereco", "Não identificado")
            
            # Enriquece com dados de experiência mais precisos
            exp_profissional = dados_estruturados.get("experiencia_profissional", {})
            if exp_profissional.get("tempo_total_experiencia_anos"):
                resultado_enriquecido["experiencia_anos"] = exp_profissional["tempo_total_experiencia_anos"]
            
            # Adiciona experiências detalhadas
            resultado_enriquecido["experiencias_detalhadas"] = exp_profissional.get("experiencias", [])
            resultado_enriquecido["areas_atuacao"] = exp_profissional.get("areas_de_atuacao", [])
            resultado_enriquecido["progressao_carreira"] = exp_profissional.get("progressao_carreira", "Não identificado")
            
            # Enriquece habilidades com dados estruturados
            habilidades = dados_estruturados.get("habilidades_competencias", {})
            if habilidades:
                resultado_enriquecido["linguagens_programacao"] = habilidades.get("linguagens_programacao", [])
                resultado_enriquecido["frameworks_bibliotecas"] = habilidades.get("frameworks_bibliotecas", [])
                resultado_enriquecido["ferramentas_devops"] = habilidades.get("ferramentas_devops", [])
                resultado_enriquecido["cloud_platforms"] = habilidades.get("cloud_platforms", [])
                resultado_enriquecido["soft_skills_identificadas"] = habilidades.get("soft_skills", [])
                resultado_enriquecido["idiomas"] = habilidades.get("idiomas", [])
                
                # Atualiza principais habilidades com dados mais precisos
                principais_hab = []
                principais_hab.extend(habilidades.get("linguagens_programacao", [])[:3])
                principais_hab.extend(habilidades.get("frameworks_bibliotecas", [])[:2])
                principais_hab.extend(habilidades.get("especializacoes", [])[:2])
                resultado_enriquecido["principais_habilidades"] = principais_hab[:5]
            
            # Adiciona formação detalhada
            formacao = dados_estruturados.get("formacao_educacao", {})
            if formacao:
                resultado_enriquecido["formacao_superior"] = formacao.get("formacao_superior", [])
                resultado_enriquecido["certificacoes_tecnicas"] = formacao.get("certificacoes", [])
                resultado_enriquecido["cursos_complementares"] = formacao.get("cursos_complementares", [])
                resultado_enriquecido["nivel_educacional"] = formacao.get("nivel_educacional", "Não identificado")
                resultado_enriquecido["area_formacao"] = formacao.get("area_formacao", "Não identificado")
            
            # Adiciona projetos e conquistas
            projetos = dados_estruturados.get("projetos_conquistas", {})
            if projetos:
                resultado_enriquecido["projetos_destaque"] = projetos.get("projetos_destaque", [])
                resultado_enriquecido["conquistas_quantificadas"] = projetos.get("conquistas_quantificadas", [])
                resultado_enriquecido["reconhecimentos"] = projetos.get("reconhecimentos", [])
                resultado_enriquecido["contribuicoes_open_source"] = projetos.get("contribuicoes_open_source", [])
            
            # Adiciona métricas calculadas pela IA
            metricas = dados_estruturados.get("metricas_calculadas", {})
            if metricas:
                resultado_enriquecido["score_completude_dados"] = metricas.get("score_completude", 0)
                resultado_enriquecido["nivel_senioridade"] = metricas.get("nivel_senioridade_calculado", "A definir")
                resultado_enriquecido["areas_especialidade"] = metricas.get("areas_especialidade", [])
                resultado_enriquecido["pontos_fortes_ia"] = metricas.get("pontos_fortes_identificados", [])
                resultado_enriquecido["gaps_identificados"] = metricas.get("gaps_identificados", [])
            
            # Adiciona informações sobre qualidade da extração
            resultado_enriquecido["qualidade_extracao_dados"] = dados_estruturados.get("qualidade_extracao", "N/A")
            resultado_enriquecido["metodo_extracao_usado"] = "IA_AVANCADA" if "IA" in dados_estruturados.get("qualidade_extracao", "") else "REGEX_BASICA"
            
            # Melhora o nível de senioridade com base nos dados estruturados
            if exp_profissional.get("tempo_total_experiencia_anos"):
                anos = exp_profissional["tempo_total_experiencia_anos"]
                if anos >= 8:
                    resultado_enriquecido["nivel_senioridade"] = "Especialista"
                elif anos >= 5:
                    resultado_enriquecido["nivel_senioridade"] = "Senior"
                elif anos >= 2:
                    resultado_enriquecido["nivel_senioridade"] = "Pleno"
                else:
                    resultado_enriquecido["nivel_senioridade"] = "Junior"
        
        return resultado_enriquecido
    
    def _formatar_dados_pessoais(self, dados: Dict) -> str:
        """Formata dados pessoais"""
        if not dados:
            return "Não disponível"
        
        formatacao = f"""
• Nome: {dados.get('nome_completo', 'Não identificado')}
• Email: {dados.get('email', 'Não identificado')}
• Telefone: {dados.get('telefone', 'Não identificado')}
• LinkedIn: {dados.get('linkedin', 'Não identificado')}
• GitHub: {dados.get('github', 'Não identificado')}
• Localização: {dados.get('endereco', 'Não identificado')}
"""
        return formatacao
    
    def _formatar_experiencia(self, experiencia: Dict) -> str:
        """Formata dados de experiência"""
        if not experiencia:
            return "Não disponível"
        
        formatacao = f"""
• Tempo total de experiência: {experiencia.get('tempo_total_experiencia_anos', 0)} anos
• Áreas de atuação: {', '.join(experiencia.get('areas_de_atuacao', []))}
• Progressão de carreira: {experiencia.get('progressao_carreira', 'Não identificado')}
• Número de experiências: {len(experiencia.get('experiencias', []))}
"""
        return formatacao
    
    def _formatar_habilidades(self, habilidades: Dict) -> str:
        """Formata habilidades"""
        if not habilidades:
            return "Não disponível"
        
        formatacao = f"""
• Linguagens: {', '.join(habilidades.get('linguagens_programacao', []))}
• Frameworks: {', '.join(habilidades.get('frameworks_bibliotecas', []))}
• Ferramentas: {', '.join(habilidades.get('ferramentas', []))}
• Nível técnico: {habilidades.get('nivel_tecnico_geral', 'Não identificado')}
• Soft Skills: {', '.join(habilidades.get('soft_skills', []))}
"""
        return formatacao
    
    def _formatar_formacao(self, formacao: Dict) -> str:
        """Formata dados de formação"""
        if not formacao:
            return "Não disponível"
        
        formatacao = f"""
• Formação superior: {len(formacao.get('formacao_superior', []))} curso(s)
• Certificações: {len(formacao.get('certificacoes', []))} certificação(ões)
• Nível educacional: {formacao.get('nivel_educacional', 'Não identificado')}
• Área de formação: {formacao.get('area_formacao', 'Não identificado')}
"""
        return formatacao
    
    def _formatar_projetos(self, projetos: Dict) -> str:
        """Formata projetos e conquistas"""
        if not projetos:
            return "Não disponível"
        
        formatacao = f"""
• Projetos destaque: {len(projetos.get('projetos_destaque', []))}
• Conquistas quantificadas: {len(projetos.get('conquistas_quantificadas', []))}
• Reconhecimentos: {len(projetos.get('reconhecimentos', []))}
• Contribuições open source: {len(projetos.get('contribuicoes_open_source', []))}
"""
        return formatacao
    
    def _formatar_metricas(self, metricas: Dict) -> str:
        """Formata métricas calculadas"""
        if not metricas:
            return "Não disponível"
        
        formatacao = f"""
• Score de completude: {metricas.get('score_completude', 0)}/100
• Nível calculado: {metricas.get('nivel_senioridade_calculado', 'Não identificado')}
• Especialidades: {', '.join(metricas.get('areas_especialidade', []))}
• Gaps identificados: {len(metricas.get('gaps_identificados', []))}
"""
        return formatacao
