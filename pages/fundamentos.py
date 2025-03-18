import streamlit as st
import pandas as pd
import yfinance as yf
import fundamentus as fd
import plotly.graph_objects as go


@st.cache_data
def get_detalhes_papel(papel):
    return fd.get_detalhes_papel(papel)


def app():
    st.title('📑 Dados Fundamentalistas')

    lista_tickers = ['PETR4', 'VALE3', 'ALOS3', 'ABEV3', 'ASAI3', 'AURE3', 'AMOB3', 'AZUL4', 'AZZA3', 'B3SA3', 'BBSE3', 'BBDC3', 'BBDC4', 
                 'BRAP4', 'BBAS3', 'BRKM5', 'BRAV3', 'BRFS3', 'BPAC11', 'CXSE3', 'CRFB3', 'CCRO3', 'CMIG4', 'COGN3', 
                 'CPLE6', 'CSAN3', 'CPFE3', 'CMIN3', 'CVCB3', 'CYRE3', 'ELET3', 'ELET6', 'EMBR3', 'ENGI11', 'ENEV3', 
                 'EGIE3', 'EQTL3', 'FLRY3', 'GGBR4', 'GOAU4', 'NTCO3', 'HAPV3', 'HYPE3', 'IGTI11', 'IRBR3', 'ISAE4', 
                 'ITSA4', 'ITUB4', 'JBSS3', 'KLBN11', 'RENT3', 'LREN3', 'LWSA3', 'MGLU3', 'POMO4', 'MRFG3', 'BEEF3', 
                 'MRVE3', 'MULT3', 'PCAR3', 'PETR3',  'RECV3', 'PRIO3', 'PETZ3', 'PSSA3', 'RADL3', 'RAIZ4', 
                 'RDOR3', 'RAIL3', 'SBSP3', 'SANB11', 'STBP3', 'SMTO3', 'CSNA3', 'SLCE3', 'SUZB3', 'TAEE11', 'VIVT3', 
                 'TIMS3', 'TOTS3', 'UGPA3', 'USIM5', 'VAMO3', 'VBBR3', 'VIVA3', 'WEGE3', 'YDUQ3']

    comparar = st.checkbox('Comparar 2 ativos')
    col1, col2  = st.columns(2)

    with col1:
        with st.expander('Ativo 1', expanded=True):
            papel1 = st.selectbox('Selecione o Papel', lista_tickers)
            st.session_state.papel1 = papel1
            info_papel1 = fd.get_detalhes_papel(papel1)
            

            st.write('**Empresa:**', info_papel1['Empresa'][0])
            st.write('**Setor:**', info_papel1['Setor'][0])
            st.write('**Subsetor:**', info_papel1['Subsetor'][0])
            st.write('**Valor de Mercado:**',f"R$ {float(info_papel1['Valor_de_mercado'][0]):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            st.write('**Nº de ações:**', f"{float(info_papel1['Nro_Acoes'][0]):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            st.write('')
            st.caption(f"Últ. balanço processado: {pd.to_datetime(info_papel1['Ult_balanco_processado'][0]).strftime('%d/%m/%Y')}")
            st.caption('Dados Balanço Patrimonial')
            st.write('**Ativo:**',f"R$ {float(info_papel1['Ativo'][0]):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            st.write('**Disponibilidades:**',f"R$ {float(info_papel1['Disponibilidades'][0]):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            st.write('**Ativo Circulante:**',f"R$ {float(info_papel1['Ativo_Circulante'][0]):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            st.write('**Dívida Bruta:**', f"R$ {float(info_papel1['Div_Bruta'][0]):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            st.write('**Dívida Líquida:**', f"R$ {float(info_papel1['Div_Liquida'][0]):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            st.write('**Patrimônio Líquido:**', f"R$ {float(info_papel1['Patrim_Liq'][0]):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            st.write('')
            st.caption('Dados demonstrativos de resultados')
            st.write('**Receita Liq. 12m:**', f"R$ {float(info_papel1['Receita_Liquida_12m'][0]):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            st.write('**EBIT. 12m:**', f"R$ {float(info_papel1['EBIT_12m'][0]):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            st.write('**Lucro Liq. 12m:**', f"R$ {float(info_papel1['Lucro_Liquido_12m'][0]):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            st.write('')            
            st.caption('Indicadores Fundamentalista')
            st.write('**P/L:**', f"{float(info_papel1['PL'][0]) / 100:,.2f}")            
            st.write('**P/VP:**', f"{float(info_papel1['PVP'][0]) / 100:,.2f}")
            st.write('**P/EBIT:**', f"{float(info_papel1['PEBIT'][0]) / 100:,.2f}")
            st.write('**LPA:**', f"{float(info_papel1['LPA'][0]) / 100:,.2f}")
            st.write('**VPA:**', f"{float(info_papel1['VPA'][0]) / 100:,.2f}")
            st.write('**EV / EBITDA:**', f"{float(info_papel1['EV_EBITDA'][0]) / 100:,.2f}")
            st.write('**EV / EBIT:**', f"{float(info_papel1['EV_EBIT'][0]) / 100:,.2f}")
            st.write('**ROIC:**', f"{(info_papel1['ROIC'][0])}")            
            st.write('**ROE:**', f"{(info_papel1['ROE'][0])}") 
            st.write('**Marg. Bruta:**', f"{(info_papel1['Marg_Bruta'][0])}") 
            st.write('**Marg. EBIT:**', f"{(info_papel1['Marg_EBIT'][0])}") 
            st.write('**Marg. Liquida:**', f"{(info_papel1['Marg_Liquida'][0])}") 
            st.write('**Div. Bruta/ Patrim.:**', f"{float(info_papel1['Div_Br_Patrim'][0])}%") 

            st.write('**Dividend Yield:**', f"{info_papel1['Div_Yield'][0]}")

    if comparar:
        with col2:
            with st.expander('Ativo 2', expanded=True):
                papel2 = st.selectbox('Selecione o 2º Papel', lista_tickers)
                info_papel2 = fd.get_detalhes_papel(papel2)
                st.write('**Empresa:**', info_papel2['Empresa'][0])
                st.write('**Setor:**', info_papel2['Setor'][0])
                st.write('**Subsetor:**', info_papel2['Subsetor'][0])
                st.write('**Valor de Mercado:**',f"R$ {float(info_papel2['Valor_de_mercado'][0]):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
                st.write('**Nº de ações:**', f"{float(info_papel2['Nro_Acoes'][0]):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))

                st.write('')
                
                st.caption(f"Últ. balanço processado: {pd.to_datetime(info_papel2['Ult_balanco_processado'][0]).strftime('%d/%m/%Y')}")
                st.caption('Dados Balanço Patrimonial')
                st.write('**Ativo:**',f"R$ {float(info_papel2['Ativo'][0]):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
                st.write('**Disponibilidades:**',f"R$ {float(info_papel2['Disponibilidades'][0]):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
                st.write('**Ativo Circulante:**',f"R$ {float(info_papel2['Ativo_Circulante'][0]):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
                st.write('**Dívida Bruta:**', f"R$ {float(info_papel2['Div_Bruta'][0]):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
                st.write('**Dívida Líquida:**', f"R$ {float(info_papel2['Div_Liquida'][0]):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
                st.write('**Patrimônio Líquido:**', f"R$ {float(info_papel2['Patrim_Liq'][0]):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
                st.write('')
                st.caption('Dados demonstrativos de resultados')
                st.write('**Receita Liq. 12m:**', f"R$ {float(info_papel2['Receita_Liquida_12m'][0]):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
                st.write('**EBIT. 12m:**', f"R$ {float(info_papel2['EBIT_12m'][0]):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
                st.write('**Lucro Liq. 12m:**', f"R$ {float(info_papel2['Lucro_Liquido_12m'][0]):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
                st.write('')            
                st.caption('Indicadores Fundamentalista')
                st.write('**P/L:**', f"{float(info_papel2['PL'][0]) / 100:,.2f}")            
                st.write('**P/VP:**', f"{float(info_papel2['PVP'][0]) / 100:,.2f}")
                st.write('**P/EBIT:**', f"{float(info_papel2['PEBIT'][0]) / 100:,.2f}")
                st.write('**LPA:**', f"{float(info_papel2['LPA'][0]) / 100:,.2f}")
                st.write('**VPA:**', f"{float(info_papel2['VPA'][0]) / 100:,.2f}")
                st.write('**EV / EBITDA:**', f"{float(info_papel2['EV_EBITDA'][0]) / 100:,.2f}")
                st.write('**EV / EBIT:**', f"{float(info_papel2['EV_EBIT'][0]) / 100:,.2f}")
                st.write('**ROIC:**', f"{(info_papel2['ROIC'][0])}")            
                st.write('**ROE:**', f"{(info_papel2['ROE'][0])}") 
                st.write('**Marg. Bruta:**', f"{(info_papel2['Marg_Bruta'][0])}") 
                st.write('**Marg. EBIT:**', f"{(info_papel2['Marg_EBIT'][0])}") 
                st.write('**Marg. Liquida:**', f"{(info_papel2['Marg_Liquida'][0])}") 
                st.write('**Div. Bruta/ Patrim.:**', f"{float(info_papel2['Div_Br_Patrim'][0])}%") 

                st.write('**Dividend Yield:**', f"{info_papel2['Div_Yield'][0]}")

   


    st.subheader('Evolução histórica')

    incluir_ibov = st.checkbox('Incluir IBOVESPA (IBOV)')

    ativos = [papel1 + '.SA']
    if comparar:
        ativos.append(papel2 + '.SA')

    if incluir_ibov:
        ativos.append('^BVSP')

    col3, col4, col00, col01 = st.columns(4)
    with col3:
        inicio = st.date_input('Data de Início', value=pd.to_datetime('2010-01-01'), format="DD/MM/YYYY")
    with col4:
        fim = st.date_input('Data de Fim', value='today', format="DD/MM/YYYY")


    if st.button('Gerar gráfico'):
        try:
            dados = yf.download(ativos, start=inicio, end=fim)['Close']

            if dados.empty:
                st.error(f'Nenhum dado foi encontrado para os ativos: {ativos} no intervalo de datas selecionado.')
            else:
                dados_pct_acumulado = (dados / dados.iloc[0] - 1) * 100

                fig = go.Figure()

                for ativo in ativos:
                    if ativo in dados_pct_acumulado.columns:
                        fig.add_trace(go.Scatter(
                            x=dados_pct_acumulado.index,
                            y=dados_pct_acumulado[ativo],
                            mode='lines',
                            name=str(ativo),  
                            line=dict(width=1)  
                        ))

                        fig.add_trace(go.Scatter(
                            x=[dados_pct_acumulado.index[-1]],  
                            y=[dados_pct_acumulado[ativo].iloc[-1]],  
                            mode='markers',
                            marker=dict(size=5, color='red', symbol='circle'),
                            name=str(ativo), 
                            showlegend=False 
                        ))

                        fig.add_annotation(
                            x=dados_pct_acumulado.index[-1], 
                            y=dados_pct_acumulado[ativo].iloc[-1], 
                            text=f'{dados_pct_acumulado[ativo].iloc[-1]:.2f}%', 
                            showarrow=True,
                            arrowhead=0,
                            ax=40,
                            ay=-40,
                            bordercolor='yellow'
                        )

                fig.update_yaxes(showgrid=True, gridwidth=0.1, gridcolor='gray', griddash='dot')
                fig.update_layout(
                    title='Histórico de Variação Percentual Acumulada dos Preços de Ativos',
                    yaxis=dict(title='Variação Percentual Acumulada (%)', side='left'),
                    legend_title='Ativos',
                    plot_bgcolor='rgba(211, 211, 211, 0.10)', 
                    xaxis=dict(showgrid=False),
                    height=600,
                    legend=dict(
                        orientation='h', 
                        y=-0.2,  
                        yanchor='bottom',  
                    )
                )

                st.plotly_chart(fig)


        except Exception as e:
            st.error(f'Ocorreu um erro: {e}')

    st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; font-size: 14px; color: #A9A9A9; margin-top: 20px;">
        <strong>Fonte:</strong> Fundamentus - Invista Consciente<br>
     
    </div>
    """, unsafe_allow_html=True)




                            