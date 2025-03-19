import streamlit as st

def app():
    st.title("Sobre o MarketView")


    st.markdown("""
    ### Visão Geral
    O MarketView é uma plataforma para acompanhamento de mercados financeiros. 
    Reúne, em um único ambiente, cotações de commodities, pares de moedas, índices de bolsas mundiais e dados fundamentalistas de ações brasileiras, 
    oferecendo uma visão ampla e integrada do cenário econômico.
    """)


    st.markdown("""
    ### Nosso Propósito
    Criei o MarketView com o objetivo de tornar a análise financeira mais acessível e eficiente. 
    Esse é o resultado de uma visão dedicada à criação de ferramentas intuitivas que ajudam investidores e profissionais a tomarem decisões informadas com base em dados atualizados e organizados.
    """)


    st.markdown("""
    ### Nosso Compromisso
    Como desenvolvedor do MarketView, estou sempre buscando formas de melhorar a experiência para todos os usuários. 
    Meu compromisso inclui a constante ampliação da base de dados, otimização de desempenho e o lançamento de funcionalidades inovadoras, 
    como alertas personalizados e integração com outras ferramentas financeiras.
    """)


    if st.button("Feedback"):
        st.markdown("Deixe seu [Feedback](https://forms.gle/M3abZwUMnBjBUi1q6)")


    if st.button("Links de Apoio"):
        st.markdown("### Links de Apoio")
        st.markdown("[Investing](https://br.investing.com/)")
        st.markdown("[InfoMoney](https://www.infomoney.com.br)")
        st.markdown("[Fundamentus](https://www.fundamentus.com.br/index.php)")
        st.markdown("[Yahoo Finance](https://finance.yahoo.com)")
        st.markdown("[TradingEconomics](https://tradingeconomics.com)")
        st.markdown("[TradingView](https://www.tradingview.com/)")
        st.markdown("[Tesouro Direto](https://www.tesourodireto.com.br/titulos/precos-e-taxas.htm#0)")