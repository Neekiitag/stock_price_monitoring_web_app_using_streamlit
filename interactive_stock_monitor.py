from datetime import datetime, timedelta
import pandas as pd
import streamlit as st
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
import pytz
import ta

# Extracting stock data based on ticker, period and interval
def fetch_stock_data(ticker, period, interval):
    end_date =datetime.now()
    if period == '1w':
        start_date = end_date - timedelta(days = 7)
        data = yf.download(ticker, start= start_date, end= end_date, interval = interval)
    else:
        data = yf.download(ticker, period = period, interval = interval)
    return data


# Transforming the data as per the timezone and making sure it has a correct format
def process_data(data):
    if data.index.tzinfo is None:
        data.index = data.index.tz_localize('UTC')
    data.index = data.index.tz_convert('US/Eastern')
    data.reset_index(inplace = True)
    data.rename(columns={'Date': 'Datetime'}, inplace=True)
    return data

# Calculating the stock metrics for analysis
def calculate_metrics(data):
    last_close = data['Close'].iloc[-1]
    prev_close = data['Close'].iloc[0]
    change = last_close - prev_close
    prct_change = (change/prev_close) * 100
    high = data['High'].max()
    low = data['Low'].min()
    volume = data['Volume'].sum()
    return last_close, prev_close, prct_change, high, low, volume


# Add simple movnf average and exponential moving average indicators
def add_technical_indicators(data):
    data['SMA_20'] = ta.trend.sma_indicator(data['Close'],window = 20)
    data['EMA_20'] = ta.trend.ema_indicator(data['Close'],window = 20)
    return data


## Part 2A : Designing webpage layout
# 1. Setting up streamlit page layout:
st.set_page_config(layout = "wide")
st.title('Real Time Stock Analysis Dashboard')

# 2. Sidebar parameters - For adding filters and user inputs

#Sidebar Information Section
st.sidebar.subheader('About')
st.sidebar.info('This dashboard provides stock data and technical indicators for various time periods. Use the sidebar to customise your view')

#Sidebar parameters
st.sidebar.header('Chart Parameters')
ticker = st.sidebar.text_input('Ticker','NVDA')
time_period = st.sidebar.selectbox('Time Period', ['1d', '1wk', '1mo', '1y', 'max'])
chart_type = st.sidebar.selectbox('Chart Type', ['Candlestick', 'Line'])
indicators = st.sidebar.multiselect('Technical Indicators', ['SMA 20', 'EMA 20'])

# 3. Mapping of time periods to data intervals
interval_mapping = {
    '1d' : '1m',
    '1wk' : '30m',
    '1mo' : '1d',
    '1y' : '1wk',
    'max' : '1wk'
}

# Part 2B : Main Content Area

# update the dashboard based on user input

if st.sidebar.button('Update'):
    data = fetch_stock_data(ticker, time_period, interval_mapping[time_period])
    data = process_data(data)
    data = add_technical_indicators(data)

    last_close, change, prct_change, high, low, volume = calculate_metrics(data)

    #display main metrics
    st.metric(label=f"{ticker} Last Price", value=f"{last_close:.2f} USD", delta=f"{change:.2f} ({prct_change:.2f}%)")

    col1, col2, col3 = st.columns(3)
    col1.metric("High", f"{high: .2f} USD")
    col2.metric("Low", f"{low: .2f} USD")
    col3.metric("Volume", f"{volume:,} ")

    #plot the stock price chart
    fig = go.Figure()
    if chart_type == 'Candlestick' : 
        fig.add_trace(go.Candlestick(x=data['Datetime'],
                                     open = data['Open'],
                                     high = data['High'],
                                     low = data['Low'],
                                     close = data['Close']))
    else:
        fig = px.line(data, x='Datetime', y='Close')

    #Add selected technical indicators to the chart
    for indicator in indicators:
        if indicator == 'SMA 20':
            fig.add_trace(go.Scatter(x=data['Datetime'], y=data['SMA_20'], name ='SMA 20'))
        elif indicator == 'EMA 20':
            fig.add_trace(go.Scatter(x=data['Datetime'], y=data['EMA_20'], name='EMA 20'))

    #FORMAT graph
    fig.update_layout(title = f'{ticker} {time_period.upper()} Chart',
                      xaxis_title = 'Time',
                      yaxis_title='Price (USD)',
                      height = 600)
    st.plotly_chart(fig, use_container_width=True)

    #display historical data and technical Indicators
    st.subheader('Historical Data')
    st.dataframe(data[['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']])

    st.subheader('Technical Indicators')
    st.dataframe(data[['Datetime', 'SMA_20', 'EMA_20']])

# PART 2C : Sidebar pricess

# Sidebar section for real-time stock prices of selected symbols
st.sidebar.header('Real-Time Stock Prices')
stock_symbols = ['META','AAPL', 'GOOGL', 'AMZN', 'MSFT', 'NFLX']
for symbol in stock_symbols:
    real_time_data = fetch_stock_data(symbol, '1d', '1m')
    if not real_time_data.empty:
        real_time_data = process_data(real_time_data)
        last_price = real_time_data['Close'].iloc[-1]
        change = last_price - real_time_data['Open'].iloc[0]
        prct_change = (change/real_time_data['Open'].iloc[0])*100
        st.sidebar.metric(f"{symbol}", f"{last_price : .2f} USD", f"{change:.2f} ({prct_change:.2f}%)")




