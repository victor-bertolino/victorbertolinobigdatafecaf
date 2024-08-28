import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px


# Função para criar conexão com o banco de dados
def get_db_connection():
    return create_engine("postgresql://postgres:YwVPdfdtNsWBjlpHrkwiCnNnsEDQGEXS@junction.proxy.rlwy.net:21088/railway")


# Função para criar tabela no PostgreSQL
def create_table(engine, df):
    df.to_sql('temperature_logs', engine, if_exists='replace', index=False)


# Upload do arquivo CSV
st.title("Upload de Arquivo CSV")
uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")

if uploaded_file is not None:
    # Leitura do arquivo CSV
    df = pd.read_csv(uploaded_file)
    st.write("Estrutura do Dataset:")
    st.write(df.head())

    # Conectar ao banco de dados
    engine = get_db_connection()

    # Criar tabela no PostgreSQL
    create_table(engine, df)
    st.success("Dados enviados para o banco de dados.")

    # Ler dados do banco de dados
    query = "SELECT * FROM temperature_logs"
    data = pd.read_sql(query, engine)

    # Visualização dos dados com Plotly
    st.title("Visualização dos Dados")
    fig = px.line(data,
                  x='noted_date',
                  y='temp',
                  title='Série Temporal de Temperaturas')
    st.plotly_chart(fig)