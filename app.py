import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import pyttsx3
from pipeline import DonationPipeline
from pathlib import Path

# Configuração inicial
st.set_page_config(page_title="Pipeline ETL - GoFundMe Simulação", layout="wide")
st.title("Pipeline ETL de Doações")
st.markdown("Simulação de um pipeline ETL inspirado na GoFundMe para centralizar e analisar dados de doações.")

# Inicializar pipeline
db_type = 'sqlite'  # Mude para 'postgres' se usar PostgreSQL
pipeline = DonationPipeline(db_type=db_type, db_name='donations.db')

# Função para feedback audível
def speak(text):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception:
        pass

# Sidebar para controles
st.sidebar.header("Controles do Pipeline")
use_api = st.sidebar.checkbox("Usar API (desmarcar para dados fictícios)", value=False)
run_button = st.sidebar.button("Executar Pipeline")
export_format = st.sidebar.selectbox("Formato de Exportação", ["csv", "json"])
export_button = st.sidebar.button("Exportar Dados")

# Estado da sessão
if 'df_transformed' not in st.session_state:
    st.session_state.df_transformed = None
if 'stats' not in st.session_state:
    st.session_state.stats = None

# Executar pipeline
if run_button:
    with st.spinner("Executando pipeline..."):
        try:
            df_transformed, stats = pipeline.run(use_api=use_api)
            st.session_state.df_transformed = df_transformed
            st.session_state.stats = stats
            st.success("Pipeline executado com sucesso!")
            speak("Pipeline executado com sucesso")
        except Exception as e:
            st.error(f"Erro: {e}")
            speak(f"Erro no pipeline: {str(e)}")

# Exibir dados
if st.session_state.df_transformed is not None:
    st.header("Dados Processados")
    st.subheader("Doações")
    st.dataframe(st.session_state.df_transformed, use_container_width=True)

    st.subheader("Estatísticas por Campanha")
    st.dataframe(st.session_state.stats, use_container_width=True)

    # Gráfico interativo
    st.subheader("Visualização")
    fig = px.bar(
        st.session_state.stats,
        x='campaign_id',
        y='total_amount',
        title="Total de Doações por Campanha",
        labels={'campaign_id': 'ID da Campanha', 'total_amount': 'Total Arrecadado (R$)'}
    )
    st.plotly_chart(fig, use_container_width=True)

# Exportar dados
if export_button and st.session_state.df_transformed is not None:
    with st.spinner("Exportando dados..."):
        try:
            output_file = pipeline.export_data(st.session_state.df_transformed, format=export_format)
            st.success(f"Dados exportados para {output_file}")
            speak(f"Dados exportados para {output_file}")
            with open(output_file, 'rb') as f:
                st.download_button(
                    label=f"Baixar {export_format.upper()}",
                    data=f,
                    file_name=output_file.name,
                    mime=f'text/{export_format}'
                )
        except Exception as e:
            st.error(f"Erro na exportação: {e}")
            speak(f"Erro na exportação: {str(e)}")

# Visualizar logs
st.sidebar.header("Logs")
if st.sidebar.button("Ver Logs"):
    log_file = Path('pipeline.log')
    if log_file.exists():
        with open(log_file, 'r') as f:
            st.text_area("Logs do Pipeline", f.read(), height=200)
    else:
        st.warning("Nenhum log disponível.")