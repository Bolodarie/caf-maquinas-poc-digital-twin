# Sistema Preditivo de Reposicao de Pecas - CAF Maquinas

Prova de Conceito (PoC) desenvolvida durante o Hackathon CAF.

## O Projeto
O sistema utiliza um "Gemeo Digital Comportamental" para simular o desgaste de pecas a partir de dados do ERP. Sem a necessidade de sensores IoT fisicos, o motor de regras cruza o Tempo de Uso, a Vida Util Padrao (MTBF) e um Fator de Severidade calibrado pelo porte da empresa cliente (CNAE).

## Detalhamento das Etapas da Arquitetura

### 1. Origem de Dados e Extracao
A arquitetura inicia-se na base instalada da CAF. O sistema nao utiliza telemetria em tempo real (IoT), garantindo viabilidade e escalabilidade imediata para as 8.500 maquinas atuais sem custo de retrofit de hardware. A extracao ocorre em modelo "Delta", processando apenas as notas fiscais e ordens de servico das ultimas 24 horas, reduzindo o custo computacional.

### 2. Enriquecimento de Dados
Para compensar a falta de sensores, o sistema utiliza inteligencia de mercado. Atraves de consultas a APIs publicas via CNPJ, o sistema identifica o CNAE do cliente. Isso permite inferir a carga de trabalho do equipamento (Fator de Severidade). Por exemplo, um moedor em um supermercado de grande porte sofre desgaste muito maior que o mesmo modelo em um pequeno acougue de bairro.

### 3. O Motor Preditivo (Gemeo Digital Comportamental)
O core do sistema e o algoritmo de decaimento desenvolvido pela equipe. Ele simula o ciclo de vida da peca considerando:
* **Delta T:** Dias ativos desde a instalacao ou ultima troca.
* **Fator de Severidade (Sf):** Multiplicador baseado no setor.
* **Uso Diario (Ud):** Horas medias trabalhadas estimadas.
* **MTBF:** Tempo Medio Entre Falhas (Mean Time Between Failures) estipulado pela engenharia da CAF.

### 4. Roteamento Inteligente
A fim de respeitar a capacidade produtiva da equipe interna e otimizar o custo de aquisicao de clientes (CAC), o funil e dividido em tres caminhos logicos:
* **Saudavel:** O ciclo de vida da peca esta normal. O sistema mantem o monitoramento silencioso.
* **Risco Iminente (Troca Preditiva):** O desgaste atingiu a margem de risco. O sistema subtrai o Lead Time logistico da CAF (12 dias) e aciona os gatilhos antes da quebra da maquina.
* **Abandono (Churn):** Se a peca ultrapassou drasticamente sua vida util teorica sem registro de compra na CAF, assume-se que ela quebrou e o cliente buscou uma peca paralela. Um alerta estrategico e gerado.

### 5. Canais de Atuacao
* **Baixo Ticket:** Pecas de desgaste natural e baixo valor agregado (como filtros e correias) nao justificam o custo da hora humana em ligacoes ativas. O sistema dispara automaticamente um webhook para plataformas de mensageria, enviando alertas preventivos pelo WhatsApp com links de compra rastreaveis para web analytics.
* **Alto Ticket:** Pecas caras e complexas geram um "Card de Contexto" no CRM. A equipe de consultores recebe a lista filtrada em ordem de criticidade, com o argumento de vendas pronto, maximizando a taxa de conversao para atingir a meta de faturamento de R$ 28 Milhoes.

## Interface e Modulos da Aplicação
Desenvolvido integralmente em Python, o prototipo consolida tres frentes de visualizacao interativa:
* **CRM (Alto Ticket):** Fila de priorizacao para a equipe de vendas focar em clientes com risco iminente de quebra ou churn.
* **Automacao (Baixo Ticket):** Simulador de disparos de Webhook para notificacoes via mensageria.
* **Portal do Cliente:** Interface interativa onde o usuario final pode simular o desgaste da sua maquina informando sua rotina de producao.

## Tecnologias Utilizadas
* **Python 3**
* **Streamlit:** Construcao do Frontend e arquitetura Multi-page App.
* **Pandas & NumPy:** Processamento de Dados, construcao do mock de ERP e calculos matematicos do Motor Preditivo.
* **CSS Customizado:** Insercao da identidade visual corporativa da CAF na interface.

## Como Rodar Localmente
1. Clone este repositorio.
2. Instale as dependencias executando: 
   ```bash
   pip install streamlit pandas numpy requests
