import streamlit as st
import time
from motor import carregar_base_processada, aplicar_estilo_caf

st.set_page_config(page_title="Automacao de Mensagens", layout="wide")
aplicar_estilo_caf()

st.header("Disparo Preditivo de Mensageria")
st.markdown("Automacao voltada para pecas de desgaste natural. Disparos categorizados como manutencao com links tagueados (UTM).")

df_processed = carregar_base_processada()
df_bot = df_processed[
    (df_processed['tipo_ticket'] == 'Baixo') & 
    (df_processed['status'] == 'Acao: Troca Imediata')
]

col_bot1, col_bot2 = st.columns([3, 1])

estilo_cabecalho = [{'selector': 'th', 'props': [('background-color', '#E6B8B8')]}]

with col_bot1:
    st.dataframe(
        df_bot[['id_cliente', 'peca', 'saude_perc', 'status']].style.set_table_styles(estilo_cabecalho), 
        use_container_width=True, 
        hide_index=True
    )

with col_bot2:
    st.write(f"**Clientes Elegiveis:** {len(df_bot)}")
    
    if st.button("Disparar Webhooks", type="primary", use_container_width=True):
        bar = st.progress(0)
        for i, (index, row) in enumerate(df_bot.iterrows()):
            payload = {
                "cliente": row['id_cliente'],
                "peca": row['peca'],
                "mensagem": f"Ola, notamos que sua peca {row['peca']} esta proxima do fim da vida util. Evite paradas na sua operacao.",
                "link_compra": f"https://cafmaquinas.com/checkout?sku={row['peca']}&utm_source=whatsapp&utm_medium=automacao_preditiva"
            }
            time.sleep(0.1) 
            bar.progress((i + 1) / len(df_bot))
            
        st.success(f"{len(df_bot)} mensagens disparadas com sucesso via Webhook!")
        with st.expander("Ver Payload do Ultimo Disparo (Simulacao)"):
            st.json(payload)