import streamlit as st
import plotly.graph_objects as go
from bcb import sgs

@st.cache_data
def get_data():
    dolar = sgs.get({'Dólar': 10813}, start='2000-01-01')
    dolar_atual = dolar.iloc[-1].values[0]
    selic = sgs.get({'Selic': 432}, start='2000-01-01')
    selic_atual = selic.iloc[-1].values[0]
    ipca = sgs.get({'IPCA': 13522}, start='2000-01-01')
    ipca_atual = ipca.iloc[-1].values[0]
    

    
    juros_real = ()
    # Calcular juros real
    

    
    return selic, selic_atual, ipca, ipca_atual, juros_real, dolar, dolar_atual

def app():
    st.title("🏛️Estatística Monetária")

    # Obtendo dados com cache
    selic, selic_atual, ipca, ipca_atual, juros_real, dolar, dolar_atual = get_data()

    col1, col2 = st.columns([5, 1])
    with col1:
        # Criando gráfico interativo da Selic
        fig_selic = go.Figure()
        fig_selic.add_trace(go.Scatter(x=selic.index, y=selic['Selic'], mode='lines'))
        fig_selic.add_trace(go.Scatter(x=[selic.index[-1]], y=[selic_atual], mode='markers', marker=dict(color='red', size=5)))

        fig_selic.update_layout(
            title='Taxa de Juros SELIC',
            title_x=0.4, 
            yaxis_title='Taxa de Juros (%)',

            showlegend=False,
            plot_bgcolor='rgba(211, 211, 211, 0.15)'  # Cor de fundo cinza claro
        )
        fig_selic.update_yaxes(showgrid=True, gridwidth=0.1, gridcolor='gray', griddash='dot', zeroline=False,  range=[0, fig_selic.data[0]['y'].max() * 1.1])
        fig_selic.update_xaxes(showgrid=False, zeroline=False)

        # Adicionando anotação para destacar o valor atual
        fig_selic.add_annotation(
            x=selic.index[-1], 
            y=selic_atual,
            text=f'{selic_atual:.2f}%',
            showarrow=True,
            arrowhead=0,
            ax=20,
            ay=-40,
            #bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='yellow'
        )
        # Criando gráfico interativo do IPCA
        fig_ipca = go.Figure()
        fig_ipca.add_trace(go.Scatter(x=ipca.index, y=ipca['IPCA'], mode='lines'))
        fig_ipca.add_trace(go.Scatter(x=[ipca.index[-1]], y=[ipca_atual], mode='markers', marker=dict(color='red', size=5)))

        fig_ipca.update_layout(
            title='IPCA Acumulado 12M',
            title_x=0.4, 
            yaxis_title='IPCA acumulado (%)',
            showlegend=False,
            plot_bgcolor='rgba(211, 211, 211, 0.15)'  # Cor de fundo cinza claro
        )
        fig_ipca.update_yaxes(showgrid=True, gridwidth=0.1, gridcolor='gray', griddash='dot',zeroline=False, range=[0, fig_ipca.data[0]['y'].max() * 1.1])
        fig_ipca.update_xaxes(showgrid=False, zeroline=False)

        # Adicionando anotação para destacar o valor atual
        fig_ipca.add_annotation(
            x=ipca.index[-1], 
            y=ipca_atual,
            text=f'{ipca_atual:.2f}%',
            showarrow=True,
            arrowhead=0,
            ax=20,
            ay=-40,
            #bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='yellow'
        )

        # Exibindo os gráficos com o Streamlit
        st.plotly_chart(fig_selic)
        st.plotly_chart(fig_ipca)

    with col2:
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        st.write('')
        
        # Exibindo o iframe com alinhamento ajustado
        iframe_code = """
        <div style="text-align: center; padding: 1px; font-family: sans-serif;">
            <span style="font-size: 20px; font-weight: bold; display: block; margin-bottom: 8px; color: white;">Mundo</span>
            <div style="display: flex; justify-content: center;">
                <iframe frameborder="0" scrolling="no" height="146" width="108" allowtransparency="true" marginwidth="0" marginheight="0" 
                src="https://sslirates.investing.com/index.php?rows=1&bg1=FFFFFF&bg2=F1F5F8&text_color=333333&enable_border=hide&border_color=0452A1&
                header_bg=ffffff&header_text=FFFFFF&force_lang=12"></iframe>
            </div>
        </div>
        """

        st.components.v1.html(iframe_code, height=180)

        juros_real = (((1 + selic_atual/100) / (1 + ipca_atual/100)) - 1) * 100

        # Exibir o resultado com alinhamento centralizado
        st.write(
            f"""
            <div style="text-align: center; color: white;">
                <h5>Juros Real:</h5>
                <span style="font-size: 35px; font-weight: normal;">{juros_real:.2f}%</span>
            </div>
            """, 
            unsafe_allow_html=True
)


    with col1:
        # Criando gráfico interativo do Dólar
        fig_dolar = go.Figure()

        fig_dolar.add_trace(go.Scatter(x=dolar.index, y=dolar['Dólar'], mode='lines', line=dict(width=1), name="Cotação do Dólar"))

        fig_dolar.add_trace(go.Scatter(x=[dolar.index[-1]], y=[dolar_atual], mode='markers', marker=dict(color='red', size=5), name="Última cotação"))

        fig_dolar.update_layout(title='Cotação do Dólar', title_x=0.4, yaxis_title='Valor em R$', showlegend=False, 
                                plot_bgcolor='rgba(211, 211, 211, 0.10)', height=550)
        
        fig_dolar.update_yaxes(showgrid=True, gridwidth=0.1, gridcolor='gray', griddash='dot', zeroline=False,
                                range=[dolar['Dólar'].min() * 0.9, dolar['Dólar'].max() * 1.1], tickformat='.2f')

        fig_dolar.update_xaxes(showgrid=False, zeroline=False)

        fig_dolar.add_annotation(x=dolar.index[-1], y=dolar_atual, text=f'R${dolar_atual:.2f}', showarrow=True,
                                arrowhead=0, ax=20, ay=-40, bordercolor='yellow')
        
        st.plotly_chart(fig_dolar)