import streamlit as st
import datetime
import pandas as pd
from motor import carregar_base_processada, aplicar_estilo_caf

st.set_page_config(page_title="Portal do Cliente", layout="wide")
aplicar_estilo_caf()

class GemeoDigitalCAF:
    def __init__(self, id_maquina, modelo, data_instalacao, setor, horas_uso_diario):
        self.id_maquina = id_maquina
        self.modelo = modelo
        self.data_instalacao = datetime.datetime.strptime(data_instalacao, "%Y-%m-%d")
        self.setor = setor
        self.horas_uso_diario = horas_uso_diario
        
        self.catalogo_mtbf = {
            "Lamina - Moedor Boca 22": 2000, 
            "Correia - Amassadeira": 4000
        }
        
        self.tabela_severidade = {
            "Supermercado (Alto Giro)": 1.5,
            "Cozinha Industrial (Medio)": 1.2,
            "Acougue/Padaria Bairro (Padrao)": 1.0
        }
        self.fator_severidade = self.tabela_severidade.get(self.setor, 1.0)

    def calcular_saude_peca(self, nome_peca, data_atual):
        mtbf_base = self.catalogo_mtbf.get(nome_peca, 2000)
        dias_ativos = (data_atual - self.data_instalacao).days
        
        desgaste_acumulado = dias_ativos * self.horas_uso_diario * self.fator_severidade
        porcentagem_saude = max(0.0, 100.0 - ((desgaste_acumulado / mtbf_base) * 100.0))
        
        horas_restantes = max(0, mtbf_base - desgaste_acumulado)
        dias_restantes = horas_restantes / (self.horas_uso_diario * self.fator_severidade) if (self.horas_uso_diario * self.fator_severidade) > 0 else 0
        data_troca = data_atual + datetime.timedelta(days=dias_restantes)

        return porcentagem_saude, data_troca, desgaste_acumulado

st.header("CAF 360: Inteligencia Preditiva")
st.markdown("Bem-vindo ao portal de gestao de ativos. Monitore a saude do seu maquinario em tempo real.")

st.markdown("### Cadastro de Equipamento")
col_in1, col_in2, col_in3, col_in4 = st.columns(4)
with col_in1:
    modelo_input = st.selectbox("Modelo da Maquina", ["Moedor Boca 22", "Amassadeira 25kg"])
with col_in2:
    setor_input = st.selectbox("Setor de Atuacao", ["Supermercado (Alto Giro)", "Cozinha Industrial (Medio)", "Acougue/Padaria Bairro (Padrao)"])
with col_in3:
    horas_input = st.slider("Horas de uso por dia", 1, 16, 6)
with col_in4:
    data_inst_input = st.date_input("Data de Instalacao", datetime.date(2026, 3, 15))

maquina = GemeoDigitalCAF(
    id_maquina="CAF-99281",
    modelo=modelo_input,
    data_instalacao=data_inst_input.strftime("%Y-%m-%d"),
    setor=setor_input,
    horas_uso_diario=horas_input
)

st.divider()

st.subheader(f"Analise de Desgaste: {maquina.modelo}")
hoje = datetime.datetime.now()

peca_alvo = "Lamina - Moedor Boca 22" if "Moedor" in modelo_input else "Correia - Amassadeira"
saude, data_troca, desgaste = maquina.calcular_saude_peca(peca_alvo, hoje)

col_met1, col_met2, col_met3 = st.columns(3)
col_met1.metric("Peca Monitorada", peca_alvo)
col_met2.metric("Vida Util Restante", f"{saude:.1f}%", help="Calculado com base na sua rotina informada no cadastro.")
col_met3.metric("Data Prevista para Troca", data_troca.strftime("%d/%m/%Y"), help="O ideal e realizar o pedido 15 dias antes desta data.")

st.markdown("### Status da Peca")
st.progress(max(0.0, min(1.0, saude / 100.0)))

if saude < 15.0:
    st.error("ALERTA CRITICO: Risco de quebra iminente. Producao pode ser interrompida.")
    st.button("Comprar Kit de Reposicao Original (15% OFF)", type="primary", key="btn_critico")
elif saude < 30.0:
    st.warning("ATENCAO: Desgaste avancado. Programe sua manutencao.")
    st.button("Agendar Entrega de Peca", key="btn_atencao")
else:
    st.success("Equipamento operando em condicoes ideais.")

st.divider()
st.markdown("### Logs do Gemeo Digital (Visao da Engenharia)")
df_logs = pd.DataFrame({
    "Metrica": ["Fator de Severidade Aplicado", "Horas de Uso Acumuladas", "MTBF Padrao (Horas)"],
    "Valor": [maquina.fator_severidade, f"{desgaste:.1f}", maquina.catalogo_mtbf.get(peca_alvo, 2000)]
})
st.table(df_logs)