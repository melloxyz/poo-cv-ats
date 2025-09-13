# 🧠 Avaliador Inteligente de Currículos

**Projeto de Programação Orientada a Objetos - CESUCA**

Sistema de análise automatizada de currículos utilizando Inteligência Artificial (Google Gemini) com interface web para otimização do processo de recrutamento.

## 📚 Sobre o Projeto

Este sistema foi desenvolvido como projeto acadêmico da disciplina de **Programação Orientada a Objetos** da faculdade **CESUCA**. O objetivo é demonstrar conceitos de POO aplicados em um sistema real que utiliza IA para automatizar a análise de currículos.

### Objetivos Acadêmicos

- Aplicação prática dos conceitos de **Programação Orientada a Objetos**
- Integração de **APIs externas** (Google Gemini AI)
- Desenvolvimento de **interface web** moderna
- Implementação de **padrões de projeto**
- **Tratamento de erros** e validações robustas

## 🚀 Funcionalidades

- **Análise de CVs**: Suporte a PDF, DOCX e TXT
- **🧠 IA Avançada**: Extração inteligente de dados com Google Gemini
- **📊 Avaliação Automática**: Score de adequação à vaga
- **🌐 Interface Web**: Sistema completo em Streamlit
- **Relatórios Detalhados**: Resultados completos com justificativas

## 🏗️ Arquitetura (POO)

### Classes Principais

- **`SistemaRecrutamento`**: Classe principal que coordena todo o sistema
- **`Curriculo`**: Responsável pelo processamento de arquivos de CV
- **`Avaliador`**: Motor de análise e avaliação usando IA
- **`GeminiClient`**: Cliente para comunicação com a API do Gemini
- **`ExtratorInteligente`**: Sistema de extração de dados em 5 passes
- **`InterfaceStreamlit`**: Interface web para o usuário

### Padrões de Projeto Utilizados

- **Factory Pattern**: Criação de objetos de processamento
- **Strategy Pattern**: Diferentes estratégias de extração
- **Observer Pattern**: Feedback de progresso na interface
- **Singleton Pattern**: Configurações do sistema

## ⚙️ Instalação e Execução

### Pré-requisitos

- Python 3.8 ou superior
- Conta Google AI Studio (gratuita)

### Instalação Rápida

1. **Execute o instalador automático**:

   ```bash
   python main.py
   ```
2. **Configure sua API Key do Gemini**:

   - Acesse: https://aistudio.google.com/
   - Crie uma API Key gratuita
   - Cole quando solicitado pelo sistema
3. **Acesse a aplicação**:

   - URL: http://localhost:8501

### Instalação Manual (Opcional)

```bash
# 1. Criar ambiente virtual
python -m venv .venv

# 2. Ativar ambiente
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Configurar API Key
echo "GEMINI_API_KEY=sua_chave_aqui" > .env

# 5. Executar
streamlit run interface_streamlit.py
```

## 📁 Estrutura do Projeto

```
📦 avaliador-curriculos/
├── 🚀 main.py                    # Ponto de entrada
├── 🌐 interface_streamlit.py     # Interface web
├── ⚙️ sistema.py                 # Classe principal
├── 📄 curriculo.py               # Processamento de CVs
├── 🧠 gemini_api.py              # Cliente IA
├── 🔍 avaliador.py               # Motor de avaliação
├── 🎯 extrator_inteligente.py    # Extração de dados
├── 📋 requirements.txt           # Dependências
└── 🔐 .env                       # Configurações
```

## Como Usar

1. **Carregue um CV** (PDF, DOCX ou TXT)
2. **Defina os requisitos da vaga** em texto livre
3. **Execute a análise** com IA
4. **Visualize os resultados** detalhados em 5 abas:
   - Dados do Candidato
   - Score de Avaliação
   - Justificativas
   - Recomendações
   - Insights Avançados

## Tecnologias Utilizadas

- **Python**: Linguagem principal
- **Streamlit**: Framework web
- **Google Gemini AI**: Motor de inteligência artificial
- **PyPDF2**: Processamento de PDFs
- **python-docx**: Processamento de documentos Word
- **Pandas**: Manipulação de dados

## 🎓 Conceitos de POO Aplicados

### Encapsulamento

- Atributos privados com métodos getter/setter
- Ocultação de implementação interna das classes

### Herança

- Classes base para diferentes tipos de processamento
- Reutilização de código através de herança

### Polimorfismo

- Métodos com comportamentos diferentes por classe
- Interface comum para diferentes implementações

### Abstração

- Classes abstratas para definir contratos
- Simplificação de interfaces complexas

## Resultados Esperados

O sistema demonstra a aplicação prática de POO em um projeto real, mostrando:

- **Modularidade**: Código organizado em classes especializadas
- **Reutilização**: Componentes reutilizáveis
- **Manutenibilidade**: Estrutura clara e documentada
- **Escalabilidade**: Arquitetura preparada para expansão

## 🔧 Troubleshooting

### Problemas Comuns

- **Erro de API**: Verifique sua chave do Gemini
- **Erro de dependência**: Execute `python main.py` novamente
- **PDF não processa**: Verifique se o PDF tem texto selecionável

## 👨‍🎓 Desenvolvimento Acadêmico

**Instituição**: CESUCA
**Disciplina**: Programação Orientada a Objetos
**Objetivo**: Aplicação prática dos conceitos de POO em projeto real

---

**🚀 Para executar: `python main.py`**
