# stock_price_monitoring_web_app_using_streamlit


This program helps to monitor the real-time stock price of a given stock. To execute this code, we need to run the following command in the Python terminal first - 

> streamlit run stock_price_monitoring_web_app_using_streamlit.py

The web page will open in your default browser. There are filtering options on the left sidebar panel, add filters like ticker symbol of stock, frequency of stock, type of graph, etc, and submit 'update'. 
This will give you the expected visual representation on the dashboard.
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

1. Designed an interactive Streamlit dashboard to provide real-time stock market insights for retail investors using Yahoo Finance data
2. Integrated yFinance API to fetch time-series data across multiple intervals and time zones for tickers like NVDA, AAPL, and MSFT
3. Implemented technical indicators such as Simple Moving Average (SMA) and Exponential Moving Average (EMA) using the ta library for trend analysis
4. Developed dynamic visualizations using Plotly (candlestick and line charts), allowing users to interactively explore historical stock performance and trends
5. Built a responsive sidebar filter for customizing ticker, time period, chart type, and technical overlays, enhancing user control and experience
6. Optimized performance by modularizing data fetching, processing, and visualization functions, ensuring scalability and easy maintenance
7. Displayed real-time metrics like price changes, volume, highs, and lows for multiple stocks, aiding quick comparative analysis on the sidebar
8. Achieved a clean, user-friendly interface and responsive layout that enabled seamless interaction with up-to-date market data
