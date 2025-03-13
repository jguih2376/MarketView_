import yfinance as yf
import requests
import pandas as pd
import pytz
import streamlit as st
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh
from datetime import datetime
import plotly.graph_objects as go

#st.set_page_config(page_title="Panorama de Mercado", layout="wide", initial_sidebar_state="collapsed")

def app():
    st.title("🌎 Panorama do Mercado")
    st.write("Visão geral do mercado atual.")

    tab1, tab2, tab3 = st.tabs (['Panorama','TradingView','Triple Screen'])

    with tab1: #Panorama

        # Configuração da página com tema escuro
        # No CSS geral (substitua a seção correspondente no início do código):
        st.markdown("""
            <style>
            .main-title {
                font-size: 36px;
                color: #FFFFFF;
                text-align: center;
                margin-bottom: 20px;
                font-weight: bold;
            }
            .subheader {
                color: #FFFFFF;
                font-size: 22px;
                margin-bottom: 15px;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 8px;
            }
            .timestamp {
                color: #A9A9A9;
                font-size: 14px;
                text-align: right;
                margin-bottom: 20px;
            }
            .card-container {
                display: flex;
                gap: 8px;
                padding: 8px;
                overflow-x: auto;
            }
            .card {
                background-color: #2E2E2E;
                border-radius: 8px;
                padding: 10px;
                width: 140px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
                text-align: center;
                transition: transform 0.2s;
                flex: 0 0 auto;
                position: relative;
                margin-bottom: 15px;
            }
            .card:hover {
                transform: scale(1.03);
                background-color: #3E3E3E;
            }
            .card-title {
                font-size: 13px;  
                color: #FFFFFF;
                margin-bottom: 4px;
                font-weight: bold;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }
            .card-value {
                font-size: 15px;  
                margin-top: 4px;
                color: #E0E0E0;
            }
            .card-variation {
                font-size: 12px;
                margin-top: 4px;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 4px;
            }
            .positive {
                color: #32CD32; /* Verde */
            }
            .negative {
                color: #FF4500; /* Vermelho */
            }
            .tooltip {
                position: relative;
                display: inline-block;
                cursor: pointer;
            }
            .tooltip .tooltiptext {
                visibility: hidden;
                width: 120px;
                background-color: #555;
                color: #fff;
                text-align: center;
                border-radius: 6px;
                padding: 5px;
                position: absolute;
                z-index: 1;
                bottom: 125%;
                left: 50%;
                margin-left: -60px;
                opacity: 0;
                transition: opacity 0.3s;
            }
            .tooltip:hover .tooltiptext {
                visibility: visible;
                opacity: 1;
            }
            /* body, .stApp {
            background-color: #1E1E1E;
            color: #FFFFFF;
            } /*
            </style>
            """, unsafe_allow_html=True)
            #body, .stApp {
            #background-color: #1E1E1E;
            #color: #FFFFFF;
            #}

        st_autorefresh(interval=10000, key="marketrefresh")

        # Ajustar para o fuso horário UTC-3
        br_tz = pytz.timezone('America/Sao_Paulo')
        br_time = datetime.now(br_tz)
       


        @st.cache_data(ttl=10)  # Moedas: 10 segundos
        def get_currency_rates():
            try:
                pairs = ["USD-BRL", "EUR-USD", "USD-JPY", "USD-GBP", "USD-CAD", "USD-SEK", "USD-CHF"]
                url = "https://economia.awesomeapi.com.br/json/last/" + ",".join(pairs)
                response = requests.get(url)
                data = response.json()
                rates = {}
                for pair in pairs:
                    pair_data = data[f"{pair.replace('-', '')}"]
                    base, quote = pair.split("-")
                    if pair == "USD-BRL":
                        rates[f"{base}/{quote}"] = float(pair_data["bid"])
                        rates[f"{base}/{quote}_pct"] = float(pair_data["pctChange"])
                    elif base == "USD":
                        rates[f"{quote}/{base}"] = 1 / float(pair_data["bid"])
                        rates[f"{quote}/{base}_pct"] = -float(pair_data["pctChange"])
                    else:
                        rates[f"{base}/{quote}"] = float(pair_data["bid"])
                        rates[f"{base}/{quote}_pct"] = float(pair_data["pctChange"])
                return pd.DataFrame([
                    {"Par": k.split("_")[0], "Cotação": v, "Variação (%)": rates[f"{k}_pct"]}
                    for k, v in rates.items() if not k.endswith("_pct")
                ])
            except Exception as e:
                st.error(f"Erro ao carregar moedas: {e}")
                return pd.DataFrame()

        @st.cache_data(ttl=1200)  # Commodities: 20 minutos
        def get_commodities():
            symbols = {
                "Metais": {'Ouro': 'GC=F', 'Prata': 'SI=F', 'Platinum': 'PL=F', 'Cobre': 'HG=F'},
                "Energia": {'WTI Oil': 'CL=F', 'Brent Oil': 'BZ=F', 'Gasolina': 'RB=F', 'Gás Natural': 'NG=F'},
                "Agrícolas": {'Gado Vivo': 'LE=F', 'Porcos Magros': 'HE=F', 'Milho': 'ZC=F', 'Soja': 'ZS=F', 'Cacau': 'CC=F', 'Café': 'KC=F'}
            }
            data = {}
            for category, items in symbols.items():
                for name, symbol in items.items():
                    try:
                        commodity = yf.Ticker(symbol)
                        hist = commodity.history(period="2d")
                        if len(hist) >= 2:
                            current_price = hist["Close"].iloc[-1]
                            prev_price = hist["Close"].iloc[-2]
                            variation = ((current_price - prev_price) / prev_price) * 100
                            data[f"{name} ({category})"] = {"Preço": round(current_price, 2), "Variação (%)": round(variation, 2)}
                        else:
                            data[f"{name} ({category})"] = {"Preço": "N/A", "Variação (%)": "N/A"}
                    except Exception as e:
                        data[f"{name} ({category})"] = {"Preço": "N/A", "Variação (%)": "N/A"}
            return pd.DataFrame([(k, v["Preço"], v["Variação (%)"]) for k, v in data.items()],
                                columns=["Commodity", "Preço", "Variação (%)"])

        @st.cache_data(ttl=1200)  # Índices: 20 minutos
        def get_stocks():
            symbols = {'IBOV': '^BVSP', 'EWZ': 'EWZ', 'S&P500': '^GSPC', 'NASDAQ': '^IXIC', 'FTSE100': '^FTSE', 
                    'DAX': '^GDAXI', 'CAC40': '^FCHI', 'SSE Composite': '000001.SS', 'Nikkei225': '^N225', 'Merval': '^MERV'}
            data = {}
            for name, symbol in symbols.items():
                try:
                    stock = yf.Ticker(symbol)
                    hist = stock.history(period="2d")
                    if len(hist) >= 2:
                        current_price = hist["Close"].iloc[-1]
                        prev_price = hist["Close"].iloc[-2]
                        variation = ((current_price - prev_price) / prev_price) * 100
                        data[name] = {"Preço": round(current_price, 2), "Variação (%)": round(variation, 2)}
                    else:
                        data[name] = {"Preço": "N/A", "Variação (%)": "N/A"}
                except Exception as e:
                    data[name] = {"Preço": "N/A", "Variação (%)": "N/A"}
            return pd.DataFrame([(k, v["Preço"], v["Variação (%)"]) for k, v in data.items()],
                                columns=["Índice", "Preço", "Variação (%)"])

        @st.cache_data(ttl=1200)  # Ações do IBOV: 20 minutos
        def get_ibov_data():
            acoes = [
                'ALOS3', 'ABEV3', 'ASAI3', 'AURE3', 'AMOB3', 'AZUL4', 'AZZA3', 'B3SA3', 'BBSE3', 'BBDC3', 'BBDC4', 
                'BRAP4', 'BBAS3', 'BRKM5', 'BRAV3', 'BRFS3', 'BPAC11', 'CXSE3', 'CRFB3', 'CCRO3', 'CMIG4', 'COGN3', 
                'CPLE6', 'CSAN3', 'CPFE3', 'CMIN3', 'CVCB3', 'CYRE3', 'ELET3', 'ELET6', 'EMBR3', 'ENGI11', 'ENEV3', 
                'EGIE3', 'EQTL3', 'FLRY3', 'GGBR4', 'GOAU4', 'NTCO3', 'HAPV3', 'HYPE3', 'IGTI11', 'IRBR3', 'ISAE4', 
                'ITSA4', 'ITUB4', 'JBSS3', 'KLBN11', 'RENT3', 'LREN3', 'LWSA3', 'MGLU3', 'POMO4', 'MRFG3', 'BEEF3', 
                'MRVE3', 'MULT3', 'PCAR3', 'PETR3', 'PETR4', 'RECV3', 'PRIO3', 'PETZ3', 'PSSA3', 'RADL3', 'RAIZ4', 
                'RDOR3', 'RAIL3', 'SBSP3', 'SANB11', 'STBP3', 'SMTO3', 'CSNA3', 'SLCE3', 'SUZB3', 'TAEE11', 'VIVT3', 
                'TIMS3', 'TOTS3', 'UGPA3', 'USIM5', 'VALE3', 'VAMO3', 'VBBR3', 'VIVA3', 'WEGE3', 'YDUQ3','BEEF3','RADL3','RDOR3'
            ]
            
            tickers = [acao + '.SA' for acao in acoes]
            data = yf.download(tickers, period="2d", interval="1d")["Close"]
            #open_data = yf.download(tickers, period="1d", interval="1d")["Open"]
            
            if data.shape[0] < 2:
                raise ValueError("Dados insuficientes para calcular a variação em relação ao dia anterior.")
            

            variacao = ((data.iloc[-1] - data.iloc[0]) / data.iloc[0]) * 100
            return pd.DataFrame({
                "Ação": [ticker[:-3] for ticker in tickers], 
                "Variação (%)": variacao.values,
                "Último Preço": data.iloc[-1].values
            })

        @st.cache_data(ttl=1200)  # Dados do IBOV: 20 minutos
        def get_stock_data(ticker, period, interval):
            stock = yf.Ticker(ticker)
            data = stock.history(period=period, interval=interval)
            return data

        # Layout principal
        col1,s, col2 = st.columns([47,1,30])

        with col1:
            with st.expander('...', expanded=True):    
                # Moedas (já ajustado anteriormente)
                st.markdown('<p class="subheader">💱 Moedas</p>', unsafe_allow_html=True)
                currency_data = get_currency_rates()
                if not currency_data.empty:
                    cols = st.columns(min(3, len(currency_data)))
                    for idx, (index, row) in enumerate(currency_data.iterrows()):
                        with cols[idx % len(cols)]:
                            var_color = "#155724" if float(row["Variação (%)"]) >= 0 else "#721c24"
                            bg_color = "#d4edda" if float(row["Variação (%)"]) >= 0 else "#f8d7da"
                            arrow = "↑" if float(row["Variação (%)"]) >= 0 else "↓"
                            st.markdown(
                                f"""
                                <div style="
                                    background-color: {bg_color}; 
                                    padding: 12px; 
                                    border-radius: 8px; 
                                    margin: 8px 0; 
                                    box-shadow: 2px 2px 4px rgba(0,0,0,0.1); 
                                    display: flex; 
                                    justify-content: space-between; 
                                    align-items: center;">
                                    <span style="font-weight: bold; font-size: 14px; color: black; flex: 1; text-align: left;">{row['Par']}</span>
                                    <span style="font-size: 12px; color: black; flex: 1; text-align: center;">{row['Cotação']:.4f}</span>
                                    <span style="font-size: 14px; color: {var_color}; font-weight: bold; flex: 1; text-align: right;">{arrow} {abs(row['Variação (%)']):.2f}%</span>
                                </div>
                                """, 
                                unsafe_allow_html=True
                            )
                st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)

                # Índices (ajustado)
                st.markdown('<p class="subheader">📈 Índices</p>', unsafe_allow_html=True)
                stocks_data = get_stocks()
                if not stocks_data.empty:
                    cols = st.columns(min(3, len(stocks_data)))
                    for idx, (index, row) in enumerate(stocks_data.iterrows()):
                        with cols[idx % len(cols)]:
                            var_value = float(str(row["Variação (%)"]).replace("N/A", "0"))
                            var_color = "#155724" if var_value >= 0 else "#721c24"
                            bg_color = "#d4edda" if var_value >= 0 else "#f8d7da"
                            arrow = "↑" if var_value >= 0 else "↓"
                            st.markdown(
                                f"""
                                <div style="
                                    background-color: {bg_color}; 
                                    padding: 12px; 
                                    border-radius: 8px; 
                                    margin: 8px 0; 
                                    box-shadow: 2px 2px 4px rgba(0,0,0,0.1); 
                                    display: flex; 
                                    justify-content: space-between; 
                                    align-items: center;">
                                    <span style="font-weight: bold; font-size: 14px; color: black; flex: 1; text-align: left;">{row['Índice']}</span>
                                    <span style="font-size: 12px; color: black; flex: 1; text-align: center;">{row['Preço']}</span>
                                    <span style="font-size: 14px; color: {var_color}; font-weight: bold; flex: 1; text-align: right;">{arrow} {abs(var_value):.2f}%</span>
                                </div>
                                """, 
                                unsafe_allow_html=True
                            )
                st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)

                # Commodities (ajustado)
                st.markdown('<p class="subheader">⛽ Commodities</p>', unsafe_allow_html=True)
                commodities_data = get_commodities()
                if not commodities_data.empty:
                    cols = st.columns(min(3, len(commodities_data) // 2 + 1))
                    for idx, (index, row) in enumerate(commodities_data.iterrows()):
                        with cols[idx % len(cols)]:
                            var_value = float(str(row["Variação (%)"]).replace("N/A", "0"))
                            var_color = "#155724" if var_value >= 0 else "#721c24"
                            bg_color = "#d4edda" if var_value >= 0 else "#f8d7da"
                            arrow = "↑" if var_value >= 0 else "↓"
                            st.markdown(
                                f"""
                                <div style="
                                    background-color: {bg_color}; 
                                    padding: 12px; 
                                    border-radius: 8px; 
                                    margin: 8px 0; 
                                    box-shadow: 2px 2px 4px rgba(0,0,0,0.1); 
                                    display: flex; 
                                    justify-content: space-between; 
                                    align-items: center;">
                                    <span style="font-weight: bold; font-size: 14px; color: black; flex: 1; text-align: left;">{row['Commodity'].split(' (')[0]}</span>
                                    <span style="font-size: 12px; color: black; flex: 1; text-align: center;">{row['Preço']}</span>
                                    <span style="font-size: 14px; color: {var_color}; font-weight: bold; flex: 1; text-align: right;">{arrow} {abs(var_value):.2f}%</span>
                                </div>
                                """, 
                                unsafe_allow_html=True
                            )
                st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)

            # Dentro do bloco `with col2:` (substitua apenas essa parte no código completo)


        with col2:
            with st.expander('...', expanded=True):
                try:
                    # Dados intraday (5 minutos)
                    intraday_data = get_stock_data('^BVSP', period="1d", interval="2m")
                    # Dados do dia anterior para fechamento e diário
                    previous_day_data = get_stock_data('^BVSP', period="2d", interval="1d")
                    # Dados semanal (5 dias úteis)
                    weekly_data = get_stock_data('^BVSP', period="1wk", interval="1d")
                    # Dados mensal (1 mês)
                    monthly_data = get_stock_data('^BVSP', period="1mo", interval="1d")
                    
                    if not intraday_data.empty and not previous_day_data.empty and not weekly_data.empty and not monthly_data.empty:
                        # Preço atual (último fechamento intraday)
                        preco_atual = intraday_data['Close'].iloc[-1]
                        # Abertura de hoje (primeiro valor do dia)
                        abertura_hoje = intraday_data['Open'].iloc[0]
                        # Fechamento do dia anterior
                        fechamento_anterior = previous_day_data['Close'].iloc[-2]   

                        # Variações
                        variacao_dia = ((preco_atual - abertura_hoje) / abertura_hoje) * 100
                        fechamento_semana_passada = weekly_data['Close'].iloc[0]
                        variacao_semanal = ((preco_atual - fechamento_semana_passada) / fechamento_semana_passada) * 100
                        fechamento_mes_passado = monthly_data['Close'].iloc[0]
                        variacao_mensal = ((preco_atual - fechamento_mes_passado) / fechamento_mes_passado) * 100


                        # Definindo a cor da linha do gráfico com base na variação do dia
                        cor_linha = '#32CD32' if variacao_dia >= 0 else '#FF4500'  # Verde mais claro e vermelho mais vibrante

                        # Gráfico de linha (intraday) com melhorias
                        fig_intraday = go.Figure()
                        fig_intraday.add_trace(go.Scatter(
                            x=intraday_data.index,
                            y=intraday_data['Close'],
                            mode='lines',
                            name="IBOV Intraday",
                            line=dict(color=cor_linha, width=1.5),  # Linha um pouco mais grossa
                            hovertemplate='%{x|%H:%M}<br>Fechamento: %{y:.2f}<extra></extra>'  # Tooltip personalizado
                        ))

                        # Adicionar anotação com o preço atual no eixo Y
                        fig_intraday.add_annotation(
                            x=1,  # Posição no extremo direito (relativo ao eixo X)
                            y=preco_atual,  # Posição no valor do preço atual (eixo Y)
                            xref="paper",  # Referência relativa ao papel (0 a 1)
                            yref="y",  # Referência ao eixo Y em valores absolutos
                            text=f"{preco_atual:.2f}",  # Texto com o preço atual formatado
                            showarrow=True,
                            arrowhead=0,
                            ax=7,  # Deslocamento horizontal da seta
                            ay=0,  # Sem deslocamento vertical
                            font=dict(size=12, color='#FFFFFF'),
                            bgcolor='rgba(0, 0, 0, 0.5)',  # Fundo semi-transparente para legibilidade
                            bordercolor='#FFFFFF',
                            borderwidth=1,
                            xanchor="left",  # Ancorar o texto à esquerda para não invadir o gráfico
                            yanchor="middle"  # Centralizar verticalmente no preço atual
                            )

                        fig_intraday.update_layout(
                            title={
                                'text': "IBOV - Intraday",
                                'y': 0.95,
                                'x': 0.5,
                                'xanchor': 'center',
                                'yanchor': 'top',
                                'font': dict(size=16, color='#FFFFFF')
                            },
                            xaxis=dict(
                                tickformat="%H:%M",  # Formato de hora
                                gridcolor='rgba(255, 255, 255, 0.1)',  # Gridlines sutis
                                zeroline=False,
                                color='#FFFFFF'
                            ),
                            yaxis=dict(
                                side="right",
                                gridcolor='rgba(255, 255, 255, 0.1)',  # Gridlines sutis
                                zeroline=False,
                                color='#FFFFFF'
                            ),
                            template="plotly_dark",
                            height=350,
                            margin=dict(l=40, r=40, t=60, b=40),  # Margens ajustadas
                            plot_bgcolor='#1E1E1E',  # Fundo do gráfico alinhado ao tema
                            paper_bgcolor='#1E1E1E',  # Fundo externo alinhado ao tema
                            font=dict(color='#FFFFFF'),  # Cor da fonte geral
                            showlegend=False,
                            legend=dict(
                                x=0.01,
                                y=0.99,
                                bgcolor='rgba(0, 0, 0, 0.5)',
                                font=dict(color='#FFFFFF')
                            )
                        )

                        st.plotly_chart(fig_intraday, use_container_width=True)

                        # Todas as variações em um único cartão (mantido como estava)
                        st.markdown(
                            f"""
                            <div style="
                                background-color: #ffffff; 
                                padding: 12px; 
                                border-radius: 8px; 
                                margin: 8px 0; 
                                box-shadow: 2px 2px 4px rgba(0,0,0,0.1);">
                                <div style="
                                    display: flex; 
                                    justify-content: space-between; 
                                    align-items: center; 
                                    margin-bottom: 8px;">
                                    <span style="font-weight: bold; font-size: 14px; color: black; flex: 1; text-align: left;">Var. do Dia</span>
                                    <span style="font-size: 12px; color: black; flex: 1; text-align: center;"></span>
                                    <span style="font-size: 14px; color: {'#155724' if variacao_dia >= 0 else '#721c24'}; font-weight: bold; flex: 1; text-align: right;">{'↑' if variacao_dia >= 0 else '↓'} {abs(variacao_dia):.2f}%</span>
                                </div>
                                <div style="
                                    display: flex; 
                                    justify-content: space-between; 
                                    align-items: center; 
                                    margin-bottom: 8px;">
                                    <span style="font-weight: bold; font-size: 14px; color: black; flex: 1; text-align: left;">Var. Semanal</span>
                                    <span style="font-size: 12px; color: black; flex: 1; text-align: center;"></span>
                                    <span style="font-size: 14px; color: {'#155724' if variacao_semanal >= 0 else '#721c24'}; font-weight: bold; flex: 1; text-align: right;">{'↑' if variacao_semanal >= 0 else '↓'} {abs(variacao_semanal):.2f}%</span>
                                </div>
                                <div style="
                                    display: flex; 
                                    justify-content: space-between; 
                                    align-items: center;">
                                    <span style="font-weight: bold; font-size: 14px; color: black; flex: 1; text-align: left;">Var. Mensal</span>
                                    <span style="font-size: 12px; color: black; flex: 1; text-align: center;"></span>
                                    <span style="font-size: 14px; color: {'#155724' if variacao_mensal >= 0 else '#721c24'}; font-weight: bold; flex: 1; text-align: right;">{'↑' if variacao_mensal >= 0 else '↓'} {abs(variacao_mensal):.2f}%</span>
                                </div>
                            </div>
                            """, 
                            unsafe_allow_html=True
                        )
                        st.markdown('')     
                    else:
                        st.warning("Nenhum dado disponível para o IBOV.")
                except Exception as e:
                    st.error(f"Erro ao carregar dados intraday: {e}")



                # Dados das ações
                try:
                    df = get_ibov_data().dropna()
                    maiores_altas = df.nlargest(5, "Variação (%)")
                    maiores_baixas = df.nsmallest(5, "Variação (%)")

                    # Layout em colunas para ações
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown(
                        """
                        <h3 style="text-align: center; font-size: 16px;">↑ Maiores Altas ↑</h3>
                        """, 
                        unsafe_allow_html=True
                    )
                        for _, row in maiores_altas.iterrows():
                            st.markdown(
                                f"""
                                <div style="
                                    background-color: #d4edda; 
                                    padding: 12px; 
                                    border-radius: 8px; 
                                    margin: 8px 0; 
                                    box-shadow: 2px 2px 4px rgba(0,0,0,0.1); 
                                    display: flex; 
                                    justify-content: space-between; 
                                    align-items: center;">
                                    <span style="font-weight: bold; font-size: 14px; color: black; flex: 1; text-align: left;">{row['Ação']}</span>
                                    <span style="font-size: 12px; color: black; flex: 1; text-align: center;">R$ {row['Último Preço']:.2f}</span>
                                    <span style="font-size: 14px; color: #155724; font-weight: bold; flex: 1; text-align: right;">{row['Variação (%)']:.2f}%</span>
                                </div>
                                """, 
                                unsafe_allow_html=True
                            )

                    with col2:
                        st.markdown(
                            """
                            <h3 style="text-align: center; font-size: 16px;">↓ Maiores Baixas ↓</h3>
                            """, 
                            unsafe_allow_html=True
                        )
                        for _, row in maiores_baixas.iterrows():
                            st.markdown(
                                f"""
                                <div style="
                                    background-color: #f8d7da; 
                                    padding: 12px; 
                                    border-radius: 8px; 
                                    margin: 8px 0; 
                                    box-shadow: 2px 2px 4px rgba(0,0,0,0.1); 
                                    display: flex; 
                                    justify-content: space-between; 
                                    align-items: center;">
                                    <span style="font-weight: bold; font-size: 14px; color: black; flex: 1; text-align: left;">{row['Ação']}</span>
                                    <span style="font-size: 12px; color: black; flex: 1; text-align: center;">R$ {row['Último Preço']:.2f}</span>
                                    <span style="font-size: 14px; color: #721c24; font-weight: bold; flex: 1; text-align: right;">{row['Variação (%)']:.2f}%</span>
                                </div>
                                """, 
                                unsafe_allow_html=True
                            )

                except Exception as e:
                    st.error(f"Erro ao carregar os dados das ações: {e}")
            # Timestamp
            st.markdown(f'<p class="timestamp">Última atualização: {br_time.strftime("%d/%m/%Y %H:%M:%S")}</p>', unsafe_allow_html=True)





        # Rodapé
        st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align: center; font-size: 12px; color: #A9A9A9; margin-top: 20px;">
            <strong>Fonte:</strong> Moedas: AwesomeAPI | Commodities, Índices e Ações: Yahoo Finance<br>
            <strong>Nota:</strong> Moedas atualizadas a cada 10 segundos; demais cotações a cada 20 minutos.
        </div>
        """, unsafe_allow_html=True)


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
        "width": "980",
        "height": "610",
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

        
    # Aba 3: Triple Screen
    with tab3:
        st.title("Triple Screen")

        # Variável para armazenar o ticker selecionado
        ticker = None

        # Seleção do ativo e tipo de gráfico dentro do expander
        with st.expander("Seleção de Ativo", expanded=True):
            opcao = st.radio('Selecione:', ['Índices', 'Ações', 'Commodities'])
            
            # Seleção do tipo de gráfico dentro do expander
            col1,col2 = st.columns([3,1])
            with col2:
                chart_type = st.selectbox("Tipo de gráfico:", ["Candlestick", "Linha"], key="chart_type")
            with col1:    
                if opcao == 'Índices':
                    indices = {
                        'IBOV': '^BVSP',
                        'S&P500': '^GSPC',     
                        'NASDAQ': '^IXIC',
                        'FTSE100': '^FTSE',
                        'DAX': '^GDAXI',
                        'CAC40': '^FCHI',
                        'SSE Composite': '000001.SS',
                        'Nikkei225': '^N225',
                        'Merval': '^MERV'
                    }
                    escolha = st.selectbox('Escolha o índice:', list(indices.keys()), index=0)
                    ticker = indices[escolha]

                elif opcao == 'Commodities':
                    commodities = {
                        'Ouro': 'GC=F',
                        'Prata': 'SI=F',
                        'Platinum': 'PL=F',     
                        'Cobre': 'HG=F',
                        'WTI Oil': 'CL=F',
                        'Brent Oil': 'BZ=F',
                        'Gasolina': 'RB=F',
                        'Gás Natural': 'NG=F',
                        'Gado Vivo': 'LE=F',
                        'Porcos Magros': 'HE=F',
                        'Milho': 'ZC=F',
                        'Soja': 'ZS=F',
                        'Cacau': 'CC=F',
                        'Café': 'KC=F'
                    }    
                    escolha = st.selectbox('Escolha o commodity:', list(commodities.keys()))
                    ticker = commodities[escolha]

                elif opcao == 'Ações':
                    acoes = ["PETR4", "VALE3", "ITUB4", "BBAS3", "BBDC4", "RAIZ4", "PRIO3", "VBBR3", "CSAN3", "UGPA3", "BPAC11", "SANB11",
                            "GGBR4", "CSNA3", "USIM5", "JBSS3", "ABEV3", "MRFG3", "BRFS3", "BEEF3", "ELET3", "NEOE3", "CPFE3", "ENGI11",
                            "EQTL3", "SUZB3", "KLBN11", "DTEX3", "RANI3", "MRFG3", "CYRE3", "MRVE3", "EZTC3", "CVCB3", "TRIS3", "WEGE3", "B3SA3"]
                    acoes_dict = {acao: acao + '.SA' for acao in acoes}
                    escolha = st.selectbox('Escolha a ação:', list(acoes_dict.keys()))
                    ticker = acoes_dict[escolha]

        # Função para obter dados da ação
        def get_stock_data(ticker, period, interval):
            stock = yf.Ticker(ticker)
            data = stock.history(period=period, interval=interval)
            return data

        # Renderizar gráficos apenas se um ticker foi selecionado
        if ticker:
            # Gráfico Diário
            try:
                daily_data = get_stock_data(ticker, period="6mo", interval="1d")
                if not daily_data.empty:
                    fig_daily = go.Figure()
                    if chart_type == "Candlestick":
                        fig_daily.add_trace(go.Candlestick(
                            x=daily_data.index,
                            open=daily_data['Open'],
                            high=daily_data['High'],
                            low=daily_data['Low'],
                            close=daily_data['Close'],
                            name="OHLC"
                        ))
                    else:  # Linha
                        fig_daily.add_trace(go.Scatter(
                            x=daily_data.index,
                            y=daily_data['Close'],
                            mode='lines',
                            name="Fechamento",
                            line=dict(color='#00ccff', width=1)
                        ))
                    fig_daily.update_layout(
                        title="Diário",
                        title_x=0.5,
                        yaxis_side="right",
                        template="plotly_dark",
                        height=700,
                        dragmode='pan',
                        xaxis=dict(
                            rangeslider=dict(visible=True, thickness=0.015),
                            rangeselector=dict(
                                buttons=list([
                                    dict(count=1, label="1m", step="month", stepmode="backward"),
                                    dict(count=3, label="3m", step="month", stepmode="backward"),
                                    dict(count=6, label="6m", step="month", stepmode="backward"),
                                    dict(count=1, label="YTD", step="year", stepmode="todate")
                                ])
                            )
                        )
                    )
                    st.plotly_chart(fig_daily, use_container_width=True)
                else:
                    st.warning("Nenhum dado diário disponível para este ticker.")
            except Exception as e:
                st.error(f"Erro ao carregar dados diários: {e}")

            # Divisão para gráficos semanal e anual
            col1, col2 = st.columns(2)

            # Gráfico Semanal
            with col1:
                try:
                    weekly_data = get_stock_data(ticker, period="1y", interval="1wk")
                    if not weekly_data.empty:
                        fig_weekly = go.Figure()
                        if chart_type == "Candlestick":
                            fig_weekly.add_trace(go.Candlestick(
                                x=weekly_data.index,
                                open=weekly_data['Open'],
                                high=weekly_data['High'],
                                low=weekly_data['Low'],
                                close=weekly_data['Close'],
                                name="OHLC"
                            ))
                        else:  # Linha
                            fig_weekly.add_trace(go.Scatter(
                                x=weekly_data.index,
                                y=weekly_data['Close'],
                                mode='lines',
                                name="Fechamento",
                                line=dict(color='#00ccff',width=1)
                            ))
                        fig_weekly.update_layout(
                            title="Semanal",
                            title_x=0.4,
                            yaxis_side="right",
                            template="plotly_dark",
                            height=450,
                            dragmode='pan',
                            xaxis=dict(
                                rangeslider=dict(visible=True, thickness=0.03),
                                rangeselector=dict(
                                    buttons=list([
                                        dict(count=1, label="1m", step="month", stepmode="backward"),
                                        dict(count=3, label="3m", step="month", stepmode="backward"),
                                        dict(count=6, label="6m", step="month", stepmode="backward"),
                                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                                        dict(step="all")
                                    ])
                                )
                            )
                        )
                        st.plotly_chart(fig_weekly, use_container_width=True)
                    else:
                        st.warning("Nenhum dado semanal disponível para este ticker.")
                except Exception as e:
                    st.error(f"Erro ao carregar dados semanais: {e}")

            # Gráfico Anual
            with col2:
                try:
                    yearly_data = get_stock_data(ticker, period="10y", interval="1mo")
                    if not yearly_data.empty:
                        fig_yearly = go.Figure()
                        if chart_type == "Candlestick":
                            fig_yearly.add_trace(go.Candlestick(
                                x=yearly_data.index,
                                open=yearly_data['Open'],
                                high=yearly_data['High'],
                                low=yearly_data['Low'],
                                close=yearly_data['Close'],
                                name="OHLC"
                            ))
                        else:  # Linha
                            fig_yearly.add_trace(go.Scatter(
                                x=yearly_data.index,
                                y=yearly_data['Close'],
                                mode='lines',
                                name="Fechamento",
                                line=dict(color='#00ccff',width=1)
                            ))
                        last_5_years = yearly_data.index[-60:]  # 5 anos * 12 meses
                        fig_yearly.update_layout(
                            title="Mensal",
                            title_x=0.4,
                            yaxis_side="right",
                            template="plotly_dark",
                            height=450,
                            dragmode='pan',
                            xaxis=dict(
                                range=[last_5_years[0], last_5_years[-1]],
                                rangeslider=dict(visible=True, thickness=0.03),
                                rangeselector=dict(
                                    buttons=list([
                                        dict(count=1, label="1a", step="year", stepmode="backward"),
                                        dict(count=3, label="3a", step="year", stepmode="backward"),
                                        dict(count=5, label="5a", step="year", stepmode="backward"),
                                        dict(count=10, label="10a", step="year", stepmode="backward"),
                                        dict(step="all")
                                    ])
                                )
                            )
                        )
                        st.plotly_chart(fig_yearly, use_container_width=True)
                    else:
                        st.warning("Nenhum dado anual disponível para este ticker.")
                except Exception as e:
                    st.error(f"Erro ao carregar dados anuais: {e}")

        else:
            st.info("Selecione um ativo e clique em 'Analisar' para visualizar os gráficos.")

        # Rodapé
        st.write("Dados fornecidos por Yahoo Finance via yfinance.")
