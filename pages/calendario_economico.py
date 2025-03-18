import streamlit as st
import streamlit.components.v1 as components



def app():
    # Título da página
    st.title("📅 Calendário Econômico")
    
    # Descrição do app
    st.write("Aqui você pode visualizar os principais eventos econômicos e dados macroeconômicos.")

    # Novo código HTML do iframe do Investing.com
    iframe_code = """
    <iframe src="https://sslecal2.investing.com?columns=exc_flags,exc_currency,exc_importance,exc_actual,exc_forecast,exc_previous&importance=2,3&features=datepicker,timezone,timeselector,filters&countries=17,32,37,5,22,39,35,4,12&calType=day&timeZone=12&lang=12" 
        width="100%" height="750" frameborder="0" allowtransparency="true" 
        marginwidth="0" marginheight="0"></iframe>
    <div class="poweredBy" style="font-family: Arial, Helvetica, sans-serif;">
        <span style="font-size: 11px;color: #333333;text-decoration: none;">
            Calendário Econômico fornecido por 
            <a href="https://br.investing.com/" rel="nofollow" target="_blank" 
            style="font-size: 11px;color: #06529D; font-weight: bold;" class="underline_link">
            Investing.com Brasil
            </a>.
        </span>
    </div>
    """
    
    # Renderizando o HTML no Streamlit
    components.html(iframe_code, height=700)


    st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; font-size: 14px; color: #A9A9A9; margin-top: 20px;">
        <strong>Fonte:</strong> Investing.com<br>
    </div>
    """, unsafe_allow_html=True)