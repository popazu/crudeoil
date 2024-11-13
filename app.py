import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
st.set_page_config(layout="wide", page_title="Vizualizare Date și Grafic")
# Citirea datelor din fișierul Excel
df = pd.read_excel('crudeoil.xlsx')

# Convertirea coloanei Date la format datetime, dacă nu este deja
df['Date'] = pd.to_datetime(df['Date'])

# Adăugarea unui radio button pentru a alege între Saptamanal, Lunar și Anual
interval_type = st.radio("Alegeți tipul de interval", ('Saptamanal', 'Lunar', 'Anual'))

# Setare slider pentru a permite selectarea intervalului de timp
if interval_type == 'Saptamanal':
    weeks = st.slider("Selectați numărul de Saptamanal pentru vizualizare", min_value=1, max_value=260, value=52)  # Max 260 Saptamanal (5 ani)
    start_date = datetime.now() - timedelta(weeks=weeks)
    df_filtered = df[df['Date'] >= start_date]
    title = f'Ultimii {weeks} Saptamanal'
elif interval_type == 'Lunar':
    months = st.slider("Selectați numărul de Lunar pentru vizualizare", min_value=1, max_value=60, value=12)  # Max 60 Lunar (5 ani)
    start_date = datetime.now() - pd.DateOffset(months=months)
    df_filtered = df[df['Date'] >= start_date]
    title = f'Ultimii {months} Lunar'
elif interval_type == 'Anual':
    years = st.slider("Selectați numărul de ani pentru vizualizare", min_value=1, max_value=5, value=1)  # Max 5 ani
    start_date = datetime.now() - pd.DateOffset(years=years)
    df_filtered = df[df['Date'] >= start_date]
    title = f'Ultimii {years} Ani'


# Selectbox pentru alegerea graficului
chart_type = st.selectbox("Alegeți tipul de grafic", ("ADX, +DI, -DI", "RSI", "Candlestick"))


# Dacă utilizatorul a ales graficul "ADX, +DI, -DI"
if chart_type == "ADX, +DI, -DI":

    fig1 = make_subplots(rows=1, cols=1, shared_xaxes=True, vertical_spacing=0.02)

    fig1.add_trace(go.Scatter(x=df_filtered['Date'], y=df_filtered['ADX'], mode='lines', name='ADX', line=dict(color='cyan')),
                    row=1, col=1)
    fig1.add_trace(go.Scatter(x=df_filtered['Date'], y=df_filtered['+DI'], mode='lines', name='+DI', line=dict(color='lightgreen'), opacity=0.7),
                    row=1, col=1)
    fig1.add_trace(go.Scatter(x=df_filtered['Date'], y=df_filtered['-DI'], mode='lines', name='-DI', line=dict(color='lightcoral'), opacity=0.7),
                    row=1, col=1)

    fig1.update_layout(
        template='plotly_dark',
        title=f'Grafic ADX, +DI, -DI - {title}',
        xaxis_title='Date',
        yaxis_title='Valoare',
        plot_bgcolor='black',
        paper_bgcolor='black'
    )

    st.plotly_chart(fig1, use_container_width=True)

# Dacă utilizatorul a ales graficul "RSI"
elif chart_type == "RSI":
    fig2 = make_subplots(rows=1, cols=1)

    fig2.add_trace(go.Scatter(
        x=df_filtered['Date'], 
        y=df_filtered['RSI'], 
        mode='lines', 
        name='RSI(14)',
        line=dict(color='yellow', width=2)
    ), row=1, col=1)

    fig2.add_hline(y=70, line=dict(color='lightgreen', dash='dash'), row=1, col=1)
    fig2.add_hline(y=30, line=dict(color='lightcoral', dash='dash'), row=1, col=1)

    fig2.update_layout(
        template='plotly_dark',
        title=f'RSI(14) - {title}',
        xaxis_title='Date',
        yaxis_title='RSI',
        plot_bgcolor='black',
        paper_bgcolor='black'
    )

    st.plotly_chart(fig2, use_container_width=True)

# Dacă utilizatorul a ales graficul "Candlestick"
elif chart_type == "Candlestick":
    fig_candlestick = go.Figure()

    # Adaugă candlestick folosind coloanele Open, High, Low, Close
    fig_candlestick.add_trace(go.Candlestick(
        x=df_filtered['Date'],
        open=df_filtered['Open'],
        high=df_filtered['High'],
        low=df_filtered['Low'],
        close=df_filtered['Price'],
        name='Candlestick'
    ))

    # Setare fundal negru și alte elemente de layout pentru graficul candlestick
    fig_candlestick.update_layout(
        template='plotly_dark',
        title=f'Grafic Candlestick ' ,
        xaxis_title='Date',
        yaxis_title='Preț',
        plot_bgcolor='black',
        paper_bgcolor='black'
    )

    st.plotly_chart(fig_candlestick, use_container_width=True)
