import streamlit as st
from motor import carregar_base_processada, aplicar_estilo_caf

st.title("CAF Maquinas - Visao Executiva (PoC)")
st.markdown("Prototipo do Gemeo Digital Comportamental para antecipacao de quebras.")

with st.expander("COMO FUNCIONA A INTELIGENCIA PREDITIVA?"):
    st.markdown("""
    O sistema nao utiliza sensores fisicos (IoT) nas maquinas. Ele calcula o desgaste real cruzando:
    * **Tempo de Uso:** Dias desde a ultima compra registrada no ERP.
    * **Fator de Severidade:** Uma carga de trabalho presumida baseada no porte da empresa (MEI, Grande, etc).
    * **MTBF (Vida Util):** O tempo padrao de falha estipulado pela engenharia da CAF.
    """)

df_processed = carregar_base_processada()
aplicar_estilo_caf()
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Receita Alvo (3 anos)", value="R$ 28M", help="Meta de business do projeto")
with col2:
    total_alertas = len(df_processed[df_processed['status'] == 'Acao: Troca Imediata'])
    st.metric(label="Pecas em Risco Critico", value=total_alertas, help="Pecas que vao quebrar nos proximos 12 dias")
with col3:
    total_churn = len(df_processed[df_processed['status'] == 'Churn / Concorrencia'])
    st.metric(label="Suspeita de Churn", value=total_churn, help="Saude negativa: a peca ja deveria ter quebrado. Se a maquina nao parou, o cliente comprou do concorrente.")
with col4:
    st.metric(label="Lead Time Logistico", value="12 Dias", help="Tempo de entrega da CAF. O alerta e gerado antes desse prazo.")

st.markdown("""
### Navegue pelo sistema no menu lateral:
* **CRM**: Fila de prioridades para ligações ativas da equipe de vendas (Alto Ticket).
* **Automacao**: Disparador de mensagens preditivas de manutencao (Baixo Ticket).
* **Portal**: Simulador da visao do cliente final acessando o diagnóstico.
""")