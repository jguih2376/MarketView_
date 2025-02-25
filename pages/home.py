import streamlit as st

def app():
     # Título da página
    st.title("📊 Bem-vindo ao MarketView!")

    # Descrição do app
    st.write('')
    st.write('')
    st.write('''
        O **MarketView** é a sua plataforma para acompanhar indicadores financeiros e econômicos.  
        Utilize o menu lateral para explorar as diversas páginas e funcionalidades do sistema, como:''')
    st.write('''
        - 📅**Calendário Econômico** - Acompanhe eventos importantes e datas chave para o mercado financeiro.''')
             
    st.write('''
        - 🌎**Panorama do Mercado** - Obtenha uma visão geral dos principais ativos. 
             - Ações Brasileira, 
             - Índices de Bolsa Mundial
             - Moedas
             - Commodities.
''')             
    st.write('''
        - 📉**Análise Histórica**
             - Retorno Mensal
             - Desempenho Relativo
''')
    st.write('''
        - 📑**Fundamentos de Ações**
             - Dados Balanço Patrimonial
             - Dados Domonstrativos de Resultados
             - Indicadores Fundamentalista
             - Performace entre ações
''')
    st.write('''
        - 🏛️**Estatística Monetária**
             - Selic
             - IPCA
             - Juros Real
             - Dólar
             
''')
        
    


