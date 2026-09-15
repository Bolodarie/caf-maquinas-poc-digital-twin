import pandas as pd
import numpy as np
import datetime
import streamlit as st

@st.cache_data
def carregar_base_processada():
    np.random.seed(42)
    
    portes = ['MEI', 'ME', 'EPP', 'Grande']
    fator_porte = {'MEI': 0.8, 'ME': 1.0, 'EPP': 1.5, 'Grande': 2.0}
    
    pecas = [
        {'nome': 'Filtro Hidraulico', 'ticket': 'Baixo', 'mtbf': 120},
        {'nome': 'Correia Dentada', 'ticket': 'Baixo', 'mtbf': 180},
        {'nome': 'Bomba de Injecao', 'ticket': 'Alto', 'mtbf': 365},
        {'nome': 'Motor de Passo', 'ticket': 'Alto', 'mtbf': 500},
        {'nome': 'Rolamento Principal', 'ticket': 'Alto', 'mtbf': 250},
    ]
    
    dados = []
    hoje = datetime.date.today()
    
    for i in range(200):
        peca = np.random.choice(pecas)
        porte = np.random.choice(portes, p=[0.2, 0.4, 0.3, 0.1])
        dias_atras = np.random.randint(10, 600)
        data_inst = hoje - datetime.timedelta(days=dias_atras)
        
        dados.append({
            "id_cliente": f"CLI-{np.random.randint(1000, 9999)}",
            "porte": porte,
            "fator_ud_sf": fator_porte[porte],
            "peca": peca['nome'],
            "tipo_ticket": peca['ticket'],
            "data_instalacao": data_inst,
            "mtbf": peca['mtbf'],
            "lead_time": 12 
        })
        
    df = pd.DataFrame(dados)
    
    # Processamento do Desgaste (alpha=1.2)
    hoje_ts = pd.Timestamp(hoje)
    df['data_instalacao'] = pd.to_datetime(df['data_instalacao'])
    df['dias_uso'] = (hoje_ts - df['data_instalacao']).dt.days
    fator_desgaste = (df['dias_uso'] * df['fator_ud_sf']) / df['mtbf']
    df['saude_perc'] = 100 * (1 - (fator_desgaste ** 1.2))
    df['saude_perc'] = df['saude_perc'].round(1)
    
    condicoes = [
        (df['saude_perc'] < -15),
        (df['saude_perc'] >= -15) & (df['saude_perc'] <= 20),
        (df['saude_perc'] > 20) & (df['saude_perc'] <= 50),
        (df['saude_perc'] > 50)
    ]
    status = ['Churn / Concorrencia', 'Acao: Troca Imediata', 'Atencao', 'Saudavel']
    df['status'] = np.select(condicoes, status, default='Indefinido')
    
    return df

def aplicar_estilo_caf():
    st.logo("logo-CAF-MAQUINAS-COLOR-1.png")
    st.markdown("""
        <style>
            /* Deixa os textos do menu lateral em maiusculo (sem mexer na cor de fundo da barra!) */
            [data-testid="stSidebarNav"] span {
                text-transform: uppercase !important;
                font-weight: 600 !important;
                letter-spacing: 1px !important;
                font-size: 14px !important;
            }
            
            /* Colore os cabecalhos das tabelas estaticas (st.table) de vermelho claro */
            [data-testid="stTable"] th {
                background-color: #E6B8B8 !important;
                color: #2B2B2B !important;
            }
        </style>
    """, unsafe_allow_html=True)