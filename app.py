import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
st.set_page_config(layout="wide")
# , page_title="Data Visualization and Chart"
# Reading data from the Excel file
df = pd.read_excel('crudeoil.xlsx')

# Converting the Date column to datetime format if not already
df['Date'] = pd.to_datetime(df['Date'])

# Adding a radio button to choose between Weekly, Monthly, and Yearly intervals
interval_type = st.radio("Select interval type", ('Weekly', 'Monthly', 'Yearly'))

# Setting a slider to allow selection of the time range
if interval_type == 'Weekly':
    weeks = st.slider("Select the number of weeks to display", min_value=1, max_value=260, value=52)  # Max 260 weeks (5 years)
    start_date = datetime.now() - timedelta(weeks=weeks)
    df_filtered = df[df['Date'] >= start_date]
    title = f'Last {weeks} Weeks'
elif interval_type == 'Monthly':
    months = st.slider("Select the number of months to display", min_value=1, max_value=60, value=12)  # Max 60 months (5 years)
    start_date = datetime.now() - pd.DateOffset(months=months)
    df_filtered = df[df['Date'] >= start_date]
    title = f'Last {months} Months'
elif interval_type == 'Yearly':
    years = st.slider("Select the number of years to display", min_value=1, max_value=5, value=1)  # Max 5 years
    start_date = datetime.now() - pd.DateOffset(years=years)
    df_filtered = df[df['Date'] >= start_date]
    title = f'Last {years} Years'

# Selectbox to choose the chart type
chart_type = st.selectbox("Select indicator to visualize", ("ADX, +DI, -DI", "RSI", "MACD", "ATR"))

# If the user chooses the "ADX, +DI, -DI" chart
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
        title=f'ADX, +DI, -DI Chart - {title}',
        xaxis_title='Date',
        yaxis_title='Value',
        plot_bgcolor='black',
        paper_bgcolor='black'
    )

    st.plotly_chart(fig1, use_container_width=True)

# If the user chooses the "RSI" chart
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

# If the user chooses the "MACD" chart
elif chart_type == "MACD":
    fig3 = make_subplots(rows=1, cols=1)

    fig3.add_trace(go.Scatter(
        x=df_filtered['Date'], 
        y=df_filtered['MACD'], 
        mode='lines', 
        name='MACD Line', 
        line=dict(color='blue')
    ), row=1, col=1)

    fig3.add_trace(go.Scatter(
        x=df_filtered['Date'], 
        y=df_filtered['MACDs'], 
        mode='lines', 
        name='Signal Line', 
        line=dict(color='red')
    ), row=1, col=1)

    fig3.add_trace(go.Bar(
        x=df_filtered['Date'], 
        y=df_filtered['MACDh'], 
        name='Histogram',
        marker=dict(color='green' if df_filtered['MACDh'].mean() > 0 else 'red')
    ), row=1, col=1)

    fig3.update_layout(
        template='plotly_dark',
        title=f'MACD Chart - {title}',
        xaxis_title='Date',
        yaxis_title='MACD',
        plot_bgcolor='black',
        paper_bgcolor='black'
    )

    st.plotly_chart(fig3, use_container_width=True)

# If the user chooses the "ATR" chart
elif chart_type == "ATR":
    fig4 = make_subplots(rows=1, cols=1)

    fig4.add_trace(go.Scatter(
        x=df_filtered['Date'], 
        y=df_filtered['ATR'], 
        mode='lines', 
        name='ATR(14)', 
        line=dict(color='orange')
    ), row=1, col=1)

    fig4.update_layout(
        template='plotly_dark',
        title=f'ATR(14) - {title}',
        xaxis_title='Date',
        yaxis_title='ATR',
        plot_bgcolor='black',
        paper_bgcolor='black'
    )

    st.plotly_chart(fig4, use_container_width=True)
