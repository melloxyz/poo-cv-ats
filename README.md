# 🧠 Avaliador Inteligente de Currículos

**Projeto de Programação Orientada a Objetos - CESUCA**

Sistema de análise automatizada de currículos utilizando Inteligência Artificial (Google Gemini) com interface web para otimização do processo de recrutamento.

## 📱 Interface do Sistema

### Tela Principal
![Interface Principal](https://i.imgur.com/SEU_LINK_1.png)
*Interface inicial do sistema com área de upload de CV e definição de requisitos da vaga*

### Análise em Andamento
![Análise em Progresso](https://i.imgur.com/SEU_LINK_2.png)
*Sistema processando o currículo com feedback visual do progresso*

### Resultados da Análise
![Resultados Detalhados](https://i.imgur.com/SEU_LINK_3.png)
*Visualização completa dos resultados com score e dados extraídos*

### Painel de Insights
![Painel de Insights](https://i.imgur.com/SEU_LINK_4.png)
*Relatórios detalhados com recomendações e justificativas da IA*

---

> **📝 Nota**: Para visualizar as imagens acima, você precisa fazer upload das suas screenshots para um serviço de hospedagem de imagens e substituir os links.

## 📚 Sobre o Projeto

Este sistema foi desenvolvido como projeto acadêmico da disciplina de **Programação Orientada a Objetos** da faculdade **CESUCA**. O objetivo é demonstrar conceitos de POO aplicados em um sistema real que utiliza IA para automatizar a análise de currículos.

### Objetivos Acadêmicos

- Aplicação prática dos conceitos de **Programação Orientada a Objetos**
- Integração de **APIs externas** (Google Gemini AI)
- Desenvolvimento de **interface web** moderna
- Implementação de **padrões de projeto**
- **Tratamento de erros** e validações robustas

## 🚀 Funcionalidades

### ✨ Principais Recursos

- **📄 Análise de CVs**: Suporte a PDF, DOCX e TXT
- **🧠 IA Avançada**: Extração inteligente de dados com Google Gemini
- **📊 Avaliação Automática**: Score de adequação à vaga (0-100%)
- **🌐 Interface Web**: Sistema completo em Streamlit
- **📈 Relatórios Detalhados**: Resultados completos com justificativas
- **🎯 Matching Inteligente**: Comparação automática com requisitos da vaga
- **💡 Recomendações**: Sugestões de melhorias para o candidato

### 📋 Dados Extraídos Automaticamente

- ✅ Informações pessoais
- ✅ Experiência profissional
- ✅ Formação acadêmica
- ✅ Habilidades técnicas
- ✅ Idiomas
- ✅ Certificações
- ✅ Score de adequação

## 🏗️ Arquitetura (POO)

### Classes Principais

```python
📦 Sistema de Classes
├── 🎯 SistemaRecrutamento    # Coordenador principal
├── 📄 Curriculo             # Processamento de arquivos
├── 🧠 Avaliador             # Motor de análise IA
├── 🔌 GeminiClient          # Cliente API Gemini
├── 🔍 ExtratorInteligente   # Extração em 5 passes
└── 🌐 InterfaceStreamlit    # Interface web
```

### Padrões de Projeto Utilizados

- **🏭 Factory Pattern**: Criação de objetos de processamento
- **🎯 Strategy Pattern**: Diferentes estratégias de extração
- **👁️ Observer Pattern**: Feedback de progresso na interface
- **🔒 Singleton Pattern**: Configurações do sistema

## ⚙️ Instalação e Execução

### 🔧 Pré-requisitos

- Python 3.8 ou superior
- Conta Google AI Studio (gratuita)

### 🚀 Instalação Rápida

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/seu-usuario/avaliador-curriculos.git
   cd avaliador-curriculos
   ```

2. **Execute o instalador automático**:
   ```bash
   python main.py
   ```

3. **Configure sua API Key do Gemini**:
   - Acesse: https://aistudio.google.com/
   - Crie uma API Key gratuita
   - Cole quando solicitado pelo sistema

4. **Acesse a aplicação**:
   - URL: http://localhost:8501

### 🛠️ Instalação Manual (Opcional)

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
├── 🔐 .env                       # Configurações
└── 📖 README.md                  # Documentação
```

## 🎮 Como Usar

### Passo a Passo

1. **📤 Upload do CV**
   - Arraste e solte ou clique para selecionar
   - Formatos suportados: PDF, DOCX, TXT

2. **📝 Definir Requisitos**
   - Descreva a vaga em texto livre
   - Inclua habilidades necessárias
   - Especifique experiência desejada

3. **🚀 Executar Análise**
   - Clique em "Analisar Currículo"
   - Acompanhe o progresso em tempo real

4. **📊 Visualizar Resultados**
   - **Aba 1**: Dados do Candidato
   - **Aba 2**: Score de Avaliação
   - **Aba 3**: Justificativas Detalhadas
   - **Aba 4**: Recomendações
   - **Aba 5**: Insights Avançados

## 🛠️ Tecnologias Utilizadas

### Backend
- ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) **Python 3.8+**
- ![Google](https://img.shields.io/badge/Google%20Gemini-4285F4?style=flat&logo=google&logoColor=white) **Google Gemini AI**
- ![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white) **Pandas**

### Frontend
- ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white) **Streamlit**

### Processamento
- **PyPDF2**: Leitura de PDFs
- **python-docx**: Documentos Word
- **Regular Expressions**: Extração de padrões

## 🎓 Conceitos de POO Aplicados

### 🔒 Encapsulamento
- Atributos privados com métodos getter/setter
- Ocultação de implementação interna das classes
- Validação de dados através de propriedades

### 🧬 Herança
- Classes base para diferentes tipos de processamento
- Reutilização de código através de herança
- Especialização de comportamentos

### 🎭 Polimorfismo
- Métodos com comportamentos diferentes por classe
- Interface comum para diferentes implementações
- Flexibilidade na extensão do sistema

### 🎯 Abstração
- Classes abstratas para definir contratos
- Simplificação de interfaces complexas
- Separação de responsabilidades

## 📈 Resultados Esperados

O sistema demonstra a aplicação prática de POO em um projeto real, mostrando:

- **📦 Modularidade**: Código organizado em classes especializadas
- **♻️ Reutilização**: Componentes reutilizáveis
- **🔧 Manutenibilidade**: Estrutura clara e documentada
- **📈 Escalabilidade**: Arquitetura preparada para expansão

## 🔧 Troubleshooting

### ❌ Problemas Comuns

| Problema | Solução |
|----------|---------|
| **Erro de API Key** | Verifique se a chave do Gemini está correta no arquivo `.env` |
| **Dependências não instaladas** | Execute `python main.py` para instalação automática |
| **PDF não processa** | Verifique se o PDF contém texto selecionável |
| **Interface não carrega** | Confirme se o Streamlit está instalado: `pip install streamlit` |
| **Erro de encoding** | Certifique-se que o arquivo está em UTF-8 |

### 📞 Suporte

Se encontrar problemas:
1. Verifique os logs no terminal
2. Confirme se todas as dependências estão instaladas
3. Teste com um CV de exemplo simples

## 🎯 Exemplos de Uso

### Caso de Uso 1: Vaga de Desenvolvedor
- **CV**: Desenvolvedor Python com 3 anos de experiência
- **Requisitos**: "Python, Django, REST APIs, banco de dados"
- **Score**: 85% - Alta compatibilidade

### Caso de Uso 2: Vaga de Designer
- **CV**: Designer gráfico com portfólio
- **Requisitos**: "Adobe Creative Suite, UX/UI, prototipação"
- **Score**: 78% - Boa compatibilidade

## 👨‍🎓 Desenvolvimento Acadêmico

**🏫 Instituição**: CESUCA
**📚 Disciplina**: Programação Orientada a Objetos
**🎯 Objetivo**: Aplicação prática dos conceitos de POO em projeto real
**👨‍🏫 Demonstração**: Sistema completo com IA e interface web

## 🚀 Próximos Passos

- [ ] Integração com banco de dados
- [ ] Sistema de relatórios avançados
- [ ] API REST para integração
- [ ] Análise de múltiplos CVs
- [ ] Dashboard de recrutamento

## 📄 Licença

Este projeto foi desenvolvido para fins acadêmicos na disciplina de Programação Orientada a Objetos do CESUCA.

---

**🚀 Para executar: `python main.py`**

**⭐ Se gostou do projeto, deixe uma estrela no GitHub!**
