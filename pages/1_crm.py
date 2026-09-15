import streamlit as st
from motor import carregar_base_processada, aplicar_estilo_caf

st.set_page_config(page_title="CRM - Alto Ticket", layout="wide")
aplicar_estilo_caf()

st.header("Fila de Priorizacao de Ligacoes (Cards de Contexto)")
st.markdown("Vendedores possuem capacidade limitada. A tabela abaixo foca apenas em **Alto Ticket** que necessita de intervencao.")

df_processed = carregar_base_processada()
df_crm = df_processed[
    (df_processed['tipo_ticket'] == 'Alto') & (df_processed['status'].isin(['Acao: Troca Imediata', 'Churn / Concorrencia']))
].sort_values(by='saude_perc')

def colorir_status(val):
    cor = 'red' if val == 'Churn / Concorrencia' else 'orange' if val == 'Acao: Troca Imediata' else 'green'
    return f'color: {cor}; font-weight: bold'

estilo_cabecalho = [{'selector': 'th', 'props': [('background-color', '#E6B8B8')]}]

st.info("""
**Guia de Abordagem para o Vendedor:**
* Linhas em **VERMELHO (Churn):** Ligue para entender se o cliente esta comprando pecas paralelas. O objetivo e reativar a conta.
* Linhas em **LARANJA (Troca Imediata):** A maquina vai parar em breve. Oferte a peca garantindo que a entrega de 12 dias chegue antes da quebra.
""")

st.dataframe(
    df_crm[['id_cliente', 'porte', 'peca', 'dias_uso', 'saude_perc', 'status']]
    .style.map(colorir_status, subset=['status'])
    .set_table_styles(estilo_cabecalho), # <-- Inserimos a cor do cabeçalho aqui
    use_container_width=True,
    hide_index=True,
    height=700
)