from iot import BACKEND
import streamlit as st
import time
import plotly.express as px
import duckdb
import pandas as pd





#Estutura da plataforma
st.set_page_config(layout="wide")
st.markdown("<h style='text-align: center; font-size: sans-serif'>PLATAFORMA PARA MONITORAMENTO IoT</h>", unsafe_allow_html=True)
relatorios = st.sidebar.multiselect("Escolha suas opções", ["Parâmetros de corrente", "Parâmetros de temperatura", "Manutenções preventivas"])



#dados
#conn = duckdb.connect('plataforma.duckdb', read_only=True)
with duckdb.connect('plataforma.duckdb') as conn:
    #Dados de corrente
    correnteTeste = conn.execute("SELECT parametro FROM correnteEletrica ORDER BY id DESC LIMIT 10").fetchall()
    horariodoTestedeCorrente = conn.execute("SELECT horariodoTeste FROM correnteEletrica ORDER BY id DESC LIMIT 10").fetchall()

    #Dados de Temperatura e umidade
    temperaturaTeste = conn.execute("SELECT valorTemperatura FROM parametroTemperatura ORDER BY id DESC LIMIT 10").fetchall()
    horariodoTestedeTemperatura = conn.execute("SELECT horariodoTeste FROM parametroTemperatura ORDER BY id DESC LIMIT 10").fetchall()
    umidadeTeste = conn.execute("SELECT valorUmidade FROM parametroTemperatura ORDER BY id DESC LIMIT 10").fetchall()

    #Dados das manutenções preventiva
    manutecaoPreventivaTeste = conn.execute("SELECT * FROM manutencaoPreventiva ORDER BY numero DESC LIMIT 10").fetchdf()
conn.close()


#Transformar os dados de corrente em listas
correnteTeste = [row[0] for row in correnteTeste]
horariodoTestedeCorrente = [row[0] for row in horariodoTestedeCorrente]

#Transforma os dados de temperatura e umidade em listas
temperaturaTeste = [row[0] for row in temperaturaTeste]
horariodoTestedeTemperatura = [row[0] for row in horariodoTestedeTemperatura]
umidadeTeste = [row[0] for row in umidadeTeste]

#Condicionais para diferenciar os gráficos

while True:
    if 'Parâmetros de corrente' in relatorios:
        st.subheader("Dados relacionados a corrente")
        fig_col1 = px.line(x=horariodoTestedeCorrente, y= correnteTeste, title="Hisórico dos parâmetros de corrente")
        st.plotly_chart(fig_col1)


    if 'Parâmetros de temperatura' in relatorios:
        st.subheader("Relatório relacionados a temperatura")
        fig_col2 = px.area(y=temperaturaTeste, x=horariodoTestedeTemperatura)
        st.plotly_chart(fig_col2)
        
        
    if 'Manutenções preventivas' in relatorios:
        st.write(manutecaoPreventivaTeste)
    BACKEND.funcaoMain()
    
    time.sleep(5)
    
    st.experimental_rerun()