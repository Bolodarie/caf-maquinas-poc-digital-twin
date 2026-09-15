# Sistema Preditivo de Reposicao de Pecas - CAF Maquinas

Prova de Conceito (PoC) desenvolvida durante o Hackathon CAF. O projeto conquistou o 1º lugar ao propor a transicao de um modelo de pos-venda reativo para um modelo preditivo baseado em dados.

## O Projeto
O sistema utiliza um "Gemeo Digital Comportamental" para simular o desgaste de pecas a partir de dados do ERP. Sem a necessidade de sensores IoT fisicos, o motor de regras cruza o Tempo de Uso, a Vida Util Padrao (MTBF) e um Fator de Severidade calibrado pelo porte da empresa cliente (CNAE).

## Arquitetura da Solucao (PoC)
Desenvolvido integralmente em Python (Streamlit e Pandas), o prototipo consolida tres frentes principais:
* **CRM (Alto Ticket):** Fila de priorizacao gerando "Cards de Contexto" para a equipe de vendas focar em clientes com risco iminente de quebra ou churn.
* **Automacao (Baixo Ticket):** Simulador de disparos de Webhook para notificacoes via WhatsApp contendo links rastreaveis (UTM) para antecipacao de manutencao.
* **Portal do Cliente:** Interface interativa onde o usuario final pode simular o desgaste da sua maquina informando sua rotina de producao.

## Tecnologias Utilizadas
* Python 3
* Streamlit (Frontend e Multi-page App)
* Pandas & NumPy (Processamento de Dados e Motor de Regras)
* Injeção de CSS customizado (Tematizacao Corporativa)

## Como Rodar Localmente
1. Clone este repositorio.
2. Instale as dependencias: `pip install streamlit pandas numpy requests`
3. Execute a aplicacao: `streamlit run app.py`
