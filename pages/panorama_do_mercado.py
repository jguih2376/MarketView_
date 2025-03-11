import streamlit as st
import streamlit.components.v1 as components

def app():
    st.title("🌎 Panorama do Mercado")
    st.write("Visão geral do mercado atual.")

    tab1, tab2, tab3 = st.tabs (['Panorama','TradingView','Triple Screen'])

    with tab1: #Panorama
        st.write('TradingView')

    with tab2: 
        st.write('TradingView')
        # HTML com o widget do TradingView
        tradingview_html = """
        <!-- TradingView Widget BEGIN -->
        <div class="tradingview-widget-container" style="height:100%;width:100%">
        <div class="tradingview-widget-container__widget" style="height:calc(100% - 32px);width:100%"></div>
        <div class="tradingview-widget-copyright"><a href="https://br.tradingview.com/" rel="noopener nofollow" target="_blank"><span class="blue-text">Monitore todos os mercados no TradingView</span></a></div>
        <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>
        {
        "autosize": true,
        "symbol": "BMFBOVESPA:IBOV",
        "timezone": "America/Sao_Paulo",
        "theme": "light",
        "style": "1",
        "locale": "br",
        "backgroundColor": "rgba(242, 242, 242, 1)",
        "withdateranges": true,
        "range": "6M",
        "hide_side_toolbar": false,
        "allow_symbol_change": false,
        "save_image": false,
        "calendar": false,
        "support_host": "https://www.tradingview.com"
        }
        </script>
        </div>
        <!-- TradingView Widget END -->
        """

        # Exibindo o widget do TradingView no Streamlit
        components.html(tradingview_html, height=600)

        
    with tab3: 
        st.write('Triple Screen')
