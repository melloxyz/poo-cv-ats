import streamlit as st
import pandas as pd
from sistema import SistemaRecrutamento
from io import StringIO
import time
from datetime import datetime

class InterfaceStreamlit:
    def __init__(self):
        self.sistema = self._obter_sistema()
        self._configurar_pagina()
    
    def _obter_sistema(self):
        # Usa sessão do Streamlit para manter o estado do sistema
        if 'sistema_recrutamento' not in st.session_state:
            st.session_state.sistema_recrutamento = SistemaRecrutamento()
        return st.session_state.sistema_recrutamento
    
    def _configurar_pagina(self):
        """
        Configura a página do Streamlit com título, ícone e layout.
        """
        st.set_page_config(
            page_title="Avaliador Inteligente de Currículos",
            page_icon="📄",
            layout="wide",
            initial_sidebar_state="collapsed"
        )
    
    def executar(self):
        """
        Executa a interface principal da aplicação.
        """
        self._renderizar_cabecalho()
        self._verificar_status_sistema()
        self._renderizar_interface_principal()
        self._renderizar_rodape()
    
    def _renderizar_cabecalho(self):
        """
        Renderiza o cabeçalho da aplicação.
        """
        st.title("🤖 Avaliador Inteligente de Currículos com IA")
        st.markdown("""
        ### Sistema avançado para análise automatizada de currículos usando IA Gemini
        
        **Como funciona:**
        1. 📤 Faça upload de um currículo (PDF ou DOCX)
        2. 📝 Descreva os requisitos da vaga
        3. 🧠 A IA analisa e gera um relatório detalhado
        4. 📊 Visualize os resultados e exporte em CSV
        """)
        
        st.markdown("---")
    
    def _verificar_status_sistema(self):
        """
        Verifica e exibe o status do sistema.
        """
        status = self.sistema.obter_status_sistema()
        
        if not status["gemini_conectado"]:
            st.error("⚠️ **Erro de Conexão**: Verifique sua chave da API Gemini no arquivo .env")
            st.stop()
    
    def _renderizar_interface_principal(self):
        """
        Renderiza a interface principal com upload e formulário.
        """
        # Container principal com duas colunas
        col_esquerda, col_direita = st.columns([1, 1])
        
        with col_esquerda:
            self._renderizar_secao_upload()
        
        with col_direita:
            self._renderizar_secao_requisitos()
        
        # Botão de análise centralizado
        self._renderizar_botao_analise()
        
        # Área de resultados
        if 'resultado_avaliacao' in st.session_state and st.session_state.resultado_avaliacao:
            st.markdown("---")
            self._renderizar_resultados()
    
    def _renderizar_secao_upload(self):
        """
        Renderiza a seção de upload de arquivo.
        """
        st.subheader("📤 Upload do Currículo")
        
        arquivo_upload = st.file_uploader(
            "Selecione o arquivo do currículo:",
            type=['pdf', 'docx'],
            help="Formatos aceitos: PDF, DOCX (máximo 10MB)",
            accept_multiple_files=False
        )
        
        if arquivo_upload is not None:
            # Armazena o arquivo na sessão
            st.session_state.arquivo_curriculo = arquivo_upload
            
            # Exibe informações do arquivo
            tamanho_mb = len(arquivo_upload.getvalue()) / (1024 * 1024)
            
            st.success(f"✅ **Arquivo carregado com sucesso!**")
            st.info(f"""
            **📋 Detalhes do arquivo:**
            - **Nome:** {arquivo_upload.name}
            - **Tipo:** {arquivo_upload.type}
            - **Tamanho:** {tamanho_mb:.2f} MB
            """)
        else:
            # Remove arquivo da sessão se não há upload
            if 'arquivo_curriculo' in st.session_state:
                del st.session_state.arquivo_curriculo
    
    def _renderizar_secao_requisitos(self):
        """
        Renderiza a seção simplificada de requisitos da vaga.
        """
        st.subheader("📝 Detalhes da Vaga")
        st.markdown("*Descreva os requisitos, atividades e informações da vaga de forma clara e direta.*")
        
        # Área de texto simples para todos os detalhes da vaga
        placeholder_texto = """As principais atividades são:

• Desenvolvimento de soluções escaláveis para nossos produtos, visando a excelência técnica
• Investigação de problemas e criação de soluções junto ao time de forma ágil
• Realização de testes e melhorias contínuas de usabilidade, performance e alta disponibilidade dos serviços

O que é essencial que você apresente:

• Ensino superior em andamento em Ciência da Computação, Engenharia da Computação, Análise e Desenvolvimento de Sistemas ou áreas afins de Tecnologia da Informação
• Desejo de trabalhar em um ambiente ágil e acelerado
• Conhecimento em Python, Django/FastAPI
• Experiência com bancos de dados relacionais (PostgreSQL, MySQL)
• Conhecimento em Git e metodologias ágeis

O que é um diferencial:

• Boa comunicação para transmitir ideias e conceitos técnicos de forma clara e eficiente
• Conhecimento relacionado ao mercado financeiro (ex: ações, opções, renda fixa, macroeconomia, HFT, criptomoedas)
• Envolvimento em projetos desafiadores e inovadores, com alto grau de complexidade
• Conhecimento em Docker, Kubernetes e cloud (AWS/Azure)
• Experiência com metodologias DevOps e CI/CD"""

        requisitos_vaga = st.text_area(
            "Requisitos e Detalhes da Vaga:",
            value=st.session_state.get('requisitos_vaga', ''),
            height=400,
            placeholder=placeholder_texto,
            help="Digite todos os detalhes da vaga: atividades, requisitos obrigatórios, diferenciais, benefícios, etc."
        )
        
        if requisitos_vaga and requisitos_vaga.strip():
            st.session_state.requisitos_vaga = requisitos_vaga
            
            # Validação básica
            num_caracteres = len(requisitos_vaga.strip())
            if num_caracteres < 50:
                st.warning(f"⚠️ Requisitos muito curtos ({num_caracteres} caracteres). Recomendado: 200+ caracteres para melhor precisão.")
            else:
                st.success(f"✅ Requisitos definidos ({num_caracteres} caracteres)")
        else:
            # Limpa os requisitos se estiver vazio
            if 'requisitos_vaga' in st.session_state:
                del st.session_state.requisitos_vaga
    
    def _renderizar_botao_analise(self):
        """
        Renderiza o botão principal de análise.
        """
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Verifica se pode executar análise
        pode_analisar = (
            'arquivo_curriculo' in st.session_state and 
            'requisitos_vaga' in st.session_state and 
            st.session_state.requisitos_vaga and
            len(st.session_state.requisitos_vaga.strip()) >= 20
        )
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(
                "🧠 **ANALISAR CURRÍCULO**", 
                disabled=not pode_analisar,
                type="primary",
                use_container_width=True,
                help="Clique para iniciar a análise inteligente do currículo"
            ):
                self._executar_analise()
        
        if not pode_analisar:
            st.warning("⚠️ Para analisar, carregue um currículo e preencha os requisitos da vaga.")
    
    def _executar_analise(self):
        """
        Executa a análise do currículo com feedback visual.
        """
        # Barra de progresso e mensagens de status
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Etapa 1: Inicializando
            status_text.text("🔄 Inicializando análise...")
            time.sleep(0.5)
            progress_bar.progress(20)
            
            # Etapa 2: Extraindo texto
            status_text.text("📄 Extraindo texto do currículo...")
            time.sleep(1)
            progress_bar.progress(40)
            
            # Etapa 3: Processando com IA
            status_text.text("🧠 Analisando com inteligência artificial...")
            time.sleep(1)
            progress_bar.progress(60)
            
            # Executa o processamento real
            resultado = self.sistema.processar_curriculo(
                st.session_state.arquivo_curriculo,
                st.session_state.requisitos_vaga
            )
            
            progress_bar.progress(80)
            status_text.text("📊 Processando resultados...")
            time.sleep(0.5)
            
            progress_bar.progress(100)
            status_text.text("✅ Análise concluída!")
            time.sleep(0.5)
            
            # Remove elementos de progresso
            progress_bar.empty()
            status_text.empty()
            
            # Verifica resultado
            if resultado["sucesso"]:
                st.session_state.resultado_avaliacao = resultado["resultado"]
                st.success("🎉 **Análise concluída com sucesso!** Veja os resultados abaixo.")
                st.rerun()
            else:
                st.error(f"❌ **Erro na análise:** {resultado['erro']}")
                if 'etapa' in resultado:
                    st.info(f"Etapa com problema: {resultado['etapa']}")
        
        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.error(f"❌ **Erro inesperado:** {str(e)}")
    
    def _renderizar_resultados(self):
        """
        Renderiza os resultados avançados da avaliação com análise completa.
        """
        st.subheader("📊 Análise Inteligente Completa")
        
        resultado = st.session_state.resultado_avaliacao
        
        # Header com score principal
        self._renderizar_header_score(resultado)
        
        # Tabs organizadas para diferentes aspectos da análise
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🎯 Visão Geral", 
            "📈 Scores Detalhados", 
            "✅ Pontos Fortes", 
            "⚠️ Pontos Fracos", 
            "📋 Relatório Completo"
        ])
        
        with tab1:
            self._renderizar_visao_geral(resultado)
        
        with tab2:
            self._renderizar_scores_detalhados(resultado)
        
        with tab3:
            self._renderizar_pontos_fortes(resultado)
        
        with tab4:
            self._renderizar_pontos_fracos(resultado)
        
        with tab5:
            self._renderizar_relatorio_completo(resultado)
        
        # Ações finais
        st.markdown("---")
        self._renderizar_acoes_finais(resultado)
    
    def _renderizar_header_score(self, resultado):
        """
        Renderiza o header com score principal e informações básicas do candidato.
        """
        score = resultado.get("score", 0)
        nome_candidato = resultado.get("nome_candidato", "Candidato")
        nivel_senioridade = resultado.get("nivel_senioridade", "N/A")
        experiencia_anos = resultado.get("experiencia_anos", "N/A")
        
        # Determina cor e classificação baseada no score
        if score >= 90:
            cor_score = "#00C851"  # Verde
            classificacao = "🌟 EXCEPCIONAL"
            emoji_reacao = "🚀"
        elif score >= 80:
            cor_score = "#2E7D32"  # Verde escuro  
            classificacao = "✅ MUITO BOM"
            emoji_reacao = "👍"
        elif score >= 70:
            cor_score = "#FF9800"  # Laranja
            classificacao = "⭐ BOM"
            emoji_reacao = "👌"
        elif score >= 60:
            cor_score = "#F57C00"  # Laranja escuro
            classificacao = "⚡ REGULAR"
            emoji_reacao = "🤔"
        elif score >= 50:
            cor_score = "#D32F2F"  # Vermelho
            classificacao = "❌ INADEQUADO"
            emoji_reacao = "😐"
        else:
            cor_score = "#B71C1C"  # Vermelho escuro
            classificacao = "🚫 REJEITADO"
            emoji_reacao = "❌"
        
        # Layout do header
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            st.markdown(f"""
            <div style="text-align: center; padding: 20px; border-radius: 15px; background: linear-gradient(135deg, {cor_score}20, {cor_score}10); border: 2px solid {cor_score};">
                <h1 style="font-size: 4em; color: {cor_score}; margin: 0; font-weight: bold;">{score}</h1>
                <p style="color: #666; margin: 0; font-weight: 500;">SCORE FINAL</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="padding: 20px; text-align: center;">
                <h2 style="color: {cor_score}; margin-bottom: 10px;">{classificacao}</h2>
                <h3 style="color: #333; margin-bottom: 5px;">{nome_candidato}</h3>
                <p style="color: #666; margin: 2px 0;"><strong>Nível:</strong> {nivel_senioridade}</p>
                <p style="color: #666; margin: 2px 0;"><strong>Experiência:</strong> {experiencia_anos} anos</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            recomendacao = resultado.get("recomendacao_contratacao", "Avaliar")
            risk_assessment = resultado.get("risk_assessment", "N/A")
            
            st.markdown(f"""
            <div style="text-align: center; padding: 20px;">
                <div style="font-size: 3em; margin-bottom: 10px;">{emoji_reacao}</div>
                <p style="color: #666; margin: 2px 0; font-size: 0.9em;"><strong>Recomendação:</strong></p>
                <p style="color: {cor_score}; margin: 2px 0; font-weight: bold; font-size: 0.9em;">{recomendacao}</p>
                <p style="color: #666; margin: 2px 0; font-size: 0.8em;"><strong>Risco:</strong> {risk_assessment}</p>
            </div>
            """, unsafe_allow_html=True)
    
    def _renderizar_visao_geral(self, resultado):
        """
        Renderiza a visão geral do candidato.
        """
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 👤 Informações do Candidato")
            
            info_container = st.container()
            with info_container:
                nome = resultado.get("nome_candidato", "Não identificado")
                email = resultado.get("email_candidato", "Não identificado")
                telefone = resultado.get("telefone_candidato", "Não identificado")
                
                st.write(f"**Nome:** {nome}")
                st.write(f"**Email:** {email}")
                st.write(f"**Telefone:** {telefone}")
            
            st.markdown("#### 🎯 Compatibilidade com a Vaga")
            compatibilidade = resultado.get("compatibilidade_vaga", resultado.get("score", 0))
            
            # Barra de progresso visual para compatibilidade
            progress_html = f"""
            <div style="background-color: #e0e0e0; border-radius: 10px; overflow: hidden; margin: 10px 0;">
                <div style="width: {compatibilidade}%; background-color: #4CAF50; height: 30px; line-height: 30px; text-align: center; color: white; font-weight: bold;">
                    {compatibilidade}%
                </div>
            </div>
            """
            st.markdown(progress_html, unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### 🚀 Principais Habilidades")
            habilidades = resultado.get("principais_habilidades", [])
            
            if habilidades:
                for i, habilidade in enumerate(habilidades[:6], 1):
                    st.markdown(f"**{i}.** {habilidade}")
            else:
                st.write("Nenhuma habilidade específica identificada")
            
            st.markdown("#### 📋 Próximos Passos Recomendados")
            proximos_passos = resultado.get("proximos_passos", [])
            
            if proximos_passos:
                for passo in proximos_passos:
                    st.markdown(f"• {passo}")
            else:
                st.write("Nenhuma recomendação específica disponível")
    
    def _renderizar_scores_detalhados(self, resultado):
        """
        Renderiza os scores detalhados por categoria.
        """
        st.markdown("#### 📊 Breakdown Detalhado dos Scores")
        
        # Verifica se há scores detalhados
        scores_detalhados = resultado.get("score_detalhado", {})
        
        if scores_detalhados:
            # Cria gráfico visual dos scores
            categories = list(scores_detalhados.keys())
            values = list(scores_detalhados.values())
            
            # Cria barras de progresso visuais para cada categoria
            for categoria, valor in scores_detalhados.items():
                # Determina cor baseada no valor
                if valor >= 80:
                    cor = "#4CAF50"  # Verde
                elif valor >= 60:
                    cor = "#FF9800"  # Laranja
                else:
                    cor = "#F44336"  # Vermelho
                
                st.markdown(f"**{categoria.title()}:** {valor}/100")
                
                progress_html = f"""
                <div style="background-color: #e0e0e0; border-radius: 10px; overflow: hidden; margin: 5px 0 15px 0;">
                    <div style="width: {valor}%; background-color: {cor}; height: 25px; line-height: 25px; text-align: center; color: white; font-weight: bold; transition: width 0.3s ease;">
                        {valor}%
                    </div>
                </div>
                """
                st.markdown(progress_html, unsafe_allow_html=True)
        else:
            st.info("Scores detalhados não disponíveis nesta avaliação.")
    
    def _renderizar_pontos_fortes(self, resultado):
        """
        Renderiza os pontos fortes identificados.
        """
        st.markdown("#### ✅ Principais Forças do Candidato")
        
        pontos_fortes = resultado.get("pontos_fortes", [])
        
        if pontos_fortes:
            for i, ponto in enumerate(pontos_fortes, 1):
                st.markdown(f"""
                <div style="background-color: #666; border-left: 4px solid #4CAF50; padding: 15px; margin: 10px 0; border-radius: 5px;">
                    <strong>✅ Ponto Forte {i}:</strong><br>
                    {ponto}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("Nenhum ponto forte específico foi identificado na avaliação.")
    
    def _renderizar_pontos_fracos(self, resultado):
        """
        Renderiza os pontos fracos e áreas de melhoria.
        """
        st.markdown("#### ⚠️ Áreas de Melhoria e Lacunas")
        
        pontos_fracos = resultado.get("pontos_fracos", [])
        
        if pontos_fracos:
            for i, ponto in enumerate(pontos_fracos, 1):
                st.markdown(f"""
                <div style="background-color: #666; border-left: 4px solid #FF9800; padding: 15px; margin: 10px 0; border-radius: 5px;">
                    <strong>⚠️ Área de Melhoria {i}:</strong><br>
                    {ponto}
                </div>
                """, unsafe_allow_html=True)
                
            st.info("💡 **Dica:** Use essas informações para planejar treinamentos ou focar em aspectos específicos durante a entrevista.")
        else:
            st.success("Nenhuma lacuna significativa foi identificada!")
    
    def _renderizar_relatorio_completo(self, resultado):
        """
        Renderiza o relatório completo da análise.
        """
        st.markdown("#### 📋 Análise Detalhada Completa")
        
        avaliacao_detalhada = resultado.get("avaliacao_detalhada", "Análise detalhada não disponível.")
        
        st.markdown(f"""
        <div style="background-color: #6666; border: 1px solid #666; border-radius: 10px; padding: 20px; line-height: 1.6;">
            {avaliacao_detalhada}
        </div>
        """, unsafe_allow_html=True)
        
        # Informações técnicas adicionais
        if resultado.get("aviso_fallback"):
            st.warning("⚠️ Esta avaliação foi realizada com sistema de backup devido a falha na API principal.")
    
    def _renderizar_acoes_finais(self, resultado):
        """
        Renderiza as ações finais disponíveis.
        """
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📄 Exportar Relatório", type="secondary", use_container_width=True):
                self._exportar_relatorio(resultado)
        
        with col2:
            if st.button("🔄 Nova Avaliação", type="secondary", use_container_width=True):
                # Limpa resultados mas mantém requisitos da vaga
                if 'resultado_avaliacao' in st.session_state:
                    del st.session_state.resultado_avaliacao
                if 'arquivo_curriculo' in st.session_state:
                    del st.session_state.arquivo_curriculo
                st.rerun()
        
        with col3:
            score = resultado.get("score", 0)
            if score >= 70:
                if st.button("📞 Agendar Entrevista", type="primary", use_container_width=True):
                    st.success("📞 Funcionalidade de agendamento será implementada em breve!")
            else:
                if st.button("📝 Dar Feedback", type="secondary", use_container_width=True):
                    st.info("📝 Funcionalidade de feedback será implementada em breve!")
    
    def _exportar_relatorio(self, resultado):
        """
        Gera relatório em formato texto para download.
        """
        relatorio = f"""
=================================================
📊 RELATÓRIO DE AVALIAÇÃO DE CURRÍCULO
=================================================

👤 CANDIDATO: {resultado.get('nome_candidato', 'Não identificado')}
📧 EMAIL: {resultado.get('email_candidato', 'Não identificado')}
📞 TELEFONE: {resultado.get('telefone_candidato', 'Não identificado')}

🎯 SCORE FINAL: {resultado.get('score', 0)}/100
📈 NÍVEL: {resultado.get('nivel_senioridade', 'N/A')}
💼 EXPERIÊNCIA: {resultado.get('experiencia_anos', 'N/A')} anos

✅ PONTOS FORTES:
"""
        
        for i, ponto in enumerate(resultado.get('pontos_fortes', []), 1):
            relatorio += f"{i}. {ponto}\n"
        
        relatorio += "\n⚠️ PONTOS FRACOS:\n"
        for i, ponto in enumerate(resultado.get('pontos_fracos', []), 1):
            relatorio += f"{i}. {ponto}\n"
        
        relatorio += f"""
📋 ANÁLISE DETALHADA:
{resultado.get('avaliacao_detalhada', 'N/A')}

🎯 RECOMENDAÇÃO: {resultado.get('recomendacao_contratacao', 'N/A')}
⚠️ AVALIAÇÃO DE RISCO: {resultado.get('risk_assessment', 'N/A')}

=================================================
Relatório gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}
=================================================
"""
        
        st.download_button(
            label="💾 Download do Relatório",
            data=relatorio,
            file_name=f"relatorio_avaliacao_{resultado.get('nome_candidato', 'candidato').replace(' ', '_')}.txt",
            mime="text/plain"
        )
    
    def _renderizar_resumo_candidato(self, resultado):
        """
        Renderiza o resumo do candidato na coluna esquerda.
        
        Args:
            resultado (Dict): Resultado da avaliação
        """
        st.markdown("### 👤 Resumo do Candidato")
        
        # Score grande e visual
        score = resultado.get("score", 0)
        classificacao = resultado.get("classificacao", "")
        
        # Determina cor baseada no score
        if score >= 80:
            cor_score = "green"
        elif score >= 60:
            cor_score = "orange"
        else:
            cor_score = "red"
        
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; border-radius: 10px; background-color: #f0f2f6;">
            <h1 style="font-size: 4em; color: {cor_score}; margin: 0;">{score}</h1>
            <h3 style="color: {cor_score}; margin: 5px 0;">{classificacao}</h3>
            <p style="color: #666; margin: 0;">Score de Aderência</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Informações do candidato
        nome_candidato = resultado.get("nome_candidato", "Não identificado")
        st.markdown(f"**👤 Candidato:** {nome_candidato}")
        
        # Pontos fortes
        pontos_fortes = resultado.get("pontos_fortes", [])
        if pontos_fortes:
            st.markdown("**✅ Principais Pontos Fortes:**")
            for ponto in pontos_fortes[:4]:
                st.markdown(f"• {ponto}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Principais habilidades
        habilidades = resultado.get("principais_habilidades", [])
        if habilidades:
            st.markdown("**🔧 Principais Habilidades:**")
            # Mostra habilidades como tags
            habilidades_text = " • ".join(habilidades[:6])
            st.markdown(f"*{habilidades_text}*")
        
        # Resumo executivo
        resumo = resultado.get("resumo", "")
        if resumo:
            st.markdown("**📝 Resumo Executivo:**")
            st.info(resumo)
    
    def _renderizar_analise_detalhada(self, resultado):
        """
        Renderiza a análise detalhada na coluna direita.
        
        Args:
            resultado (Dict): Resultado da avaliação
        """
        st.markdown("### 📋 Análise Detalhada")
        
        # Avaliação completa
        avaliacao_detalhada = resultado.get("avaliacao_detalhada", "")
        if avaliacao_detalhada:
            st.markdown("**🧠 Avaliação Completa da IA:**")
            st.markdown(avaliacao_detalhada)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Pontos fracos/melhorias
        pontos_fracos = resultado.get("pontos_fracos", [])
        if pontos_fracos:
            st.markdown("**⚠️ Pontos de Melhoria:**")
            for ponto in pontos_fracos:
                st.markdown(f"• {ponto}")
        
        # Informações técnicas (expansível)
        with st.expander("🔍 Informações Técnicas", expanded=False):
            metadados_arquivo = resultado.get("metadados_arquivo", {})
            metadados_proc = resultado.get("metadados_processamento", {})
            
            st.markdown("**Arquivo processado:**")
            st.write(f"• Nome: {metadados_arquivo.get('nome_arquivo', 'N/A')}")
            st.write(f"• Tipo: {metadados_arquivo.get('tipo_arquivo', 'N/A')}")
            st.write(f"• Tamanho: {metadados_arquivo.get('tamanho_mb', 0):.2f} MB")
            
            st.markdown("**Processamento:**")
            data_proc = metadados_proc.get('data_avaliacao', '')
            if data_proc:
                data_formatada = datetime.fromisoformat(data_proc.replace('Z', '+00:00')).strftime('%d/%m/%Y %H:%M:%S')
                st.write(f"• Data: {data_formatada}")
            st.write(f"• Versão: {metadados_proc.get('versao_sistema', 'N/A')}")
    
    def _renderizar_botao_exportacao(self):
        """
        Renderiza o botão de exportação em CSV.
        """
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col2:
            if st.button("📥 **Exportar Análise em CSV**", type="secondary", use_container_width=True):
                self._exportar_csv()
    
    def _exportar_csv(self):
        """
        Executa a exportação dos dados em CSV.
        """
        try:
            df_resultado = self.sistema.exportar_resultado_csv()
            
            if df_resultado is not None:
                # Converte DataFrame para CSV
                csv_buffer = StringIO()
                df_resultado.to_csv(csv_buffer, index=False, encoding='utf-8-sig')
                csv_data = csv_buffer.getvalue()
                
                # Nome do arquivo com timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                nome_arquivo = f"avaliacao_curriculo_{timestamp}.csv"
                
                # Botão de download
                st.download_button(
                    label="⬇️ Download CSV",
                    data=csv_data,
                    file_name=nome_arquivo,
                    mime="text/csv",
                    help="Clique para baixar a análise em formato CSV"
                )
                
                st.success("✅ CSV gerado com sucesso! Clique no botão acima para baixar.")
            else:
                st.error("❌ Erro ao gerar CSV. Tente novamente.")
                
        except Exception as e:
            st.error(f"❌ Erro na exportação: {str(e)}")
    
    def _renderizar_rodape(self):
        """
        Renderiza o rodapé da aplicação.
        """
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #666; padding: 20px;">
            <p>🤖 <b>Avaliador Inteligente de Currículos</b> | Powered by Gemini AI</p>
            <p><i>Sistema desenvolvido com Python, Streamlit e programação orientada a objetos</i></p>
        </div>
        """, unsafe_allow_html=True)

# Função principal para execução
def main():
    """
    Função principal para executar a aplicação Streamlit.
    """
    try:
        interface = InterfaceStreamlit()
        interface.executar()
    except Exception as e:
        st.error(f"Erro fatal na aplicação: {str(e)}")
        st.info("Verifique se todas as dependências estão instaladas e o arquivo .env está configurado corretamente.")

if __name__ == "__main__":
    main()