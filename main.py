#!/usr/bin/env python3
"""
Avaliador Inteligente de Currículos
Projeto POO - CESUCA
"""

import sys
import os
import streamlit as st

def verificar_dependencias():
    """Verifica se dependências estão instaladas"""
    dependencias_requeridas = [
        'streamlit',
        'PyPDF2', 
        'docx',
        'dotenv',
        'google.genai',
        'pandas'
    ]
    
    dependencias_faltando = []
    
    for dep in dependencias_requeridas:
        try:
            __import__(dep.replace('-', '_'))
        except ImportError:
            dependencias_faltando.append(dep)
    
    return len(dependencias_faltando) == 0, dependencias_faltando

def verificar_arquivo_env():
    """
    Verifica se o arquivo .env existe e contém as variáveis necessárias.
    
    Returns:
        tuple: (bool, str) - (sucesso, mensagem)
    """
    if not os.path.exists('.env'):
        return False, "Arquivo .env não encontrado"
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        if not os.getenv('GEMINI_API_KEY'):
            return False, "GEMINI_API_KEY não definida no arquivo .env"
        
        return True, "Arquivo .env configurado corretamente"
    
    except Exception as e:
        return False, f"Erro ao carregar .env: {str(e)}"

def exibir_erro_configuracao():
    """Exibe página de erro de configuração"""
    st.set_page_config(
        page_title="Erro de Configuração",
        page_icon="⚠️",
        layout="centered"
    )
    
    st.error("⚠️ **Erro de Configuração**")
    
    deps_ok, deps_faltando = verificar_dependencias()
    
    if not deps_ok:
        st.error("**Dependências faltando:**")
        for dep in deps_faltando:
            st.write(f"❌ {dep}")
        
        st.info("""
        **Para instalar as dependências:**
        ```bash
        pip install streamlit PyPDF2 python-docx python-dotenv google-genai pandas
        ```
        """)
    
    env_ok, env_msg = verificar_arquivo_env()
    
    if not env_ok:
        st.error(f"**Arquivo .env:** {env_msg}")
        
        st.info("""
        **Para configurar o arquivo .env:**
        
        1. Crie um arquivo chamado `.env` na pasta do projeto
        2. Adicione sua chave da API Gemini:
        
        ```
        GEMINI_API_KEY=sua_chave_aqui
        ```
        
        3. Obtenha sua chave em: https://ai.google.dev/
        """)
    
    st.warning("Corrija os problemas acima e reinicie a aplicação.")

def main():
    """
    Função principal - ponto de entrada da aplicação.
    """
    # Verifica configuração básica
    deps_ok, _ = verificar_dependencias()
    env_ok, _ = verificar_arquivo_env()
    
    if not deps_ok or not env_ok:
        exibir_erro_configuracao()
        return
    
    # Se tudo estiver OK, executa a aplicação
    try:
        from interface_streamlit import main as executar_interface
        executar_interface()
        
    except ImportError as e:
        st.error(f"❌ Erro ao importar módulos: {str(e)}")
        st.info("Verifique se todos os arquivos do projeto estão no diretório correto.")
    
    except Exception as e:
        st.error(f"❌ Erro na aplicação: {str(e)}")
        st.info("Verifique os logs do console para mais detalhes.")

if __name__ == "__main__":
    # Informações do sistema
    print("=" * 60)
    print("🤖 AVALIADOR INTELIGENTE DE CURRÍCULOS COM IA")
    print("=" * 60)
    print(f"Python: {sys.version}")
    print(f"Diretório: {os.getcwd()}")
    print("=" * 60)
    
    # Executa verificações iniciais
    print("🔍 Verificando configuração...")
    
    deps_ok, deps_faltando = verificar_dependencias()
    if deps_ok:
        print("✅ Dependências: OK")
    else:
        print(f"❌ Dependências faltando: {', '.join(deps_faltando)}")
    
    env_ok, env_msg = verificar_arquivo_env()
    if env_ok:
        print("✅ Arquivo .env: OK")
    else:
        print(f"❌ Arquivo .env: {env_msg}")
    
    if deps_ok and env_ok:
        print("🚀 Iniciando aplicação...")
    else:
        print("⚠️ Problemas de configuração detectados")
    
    print("=" * 60)
    
    # Executa aplicação
    main()