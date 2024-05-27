import streamlit as st
from datetime import date
import numpy as np
import pandas as pd
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
from dateutil.parser import parse



def main():
    # Define START and TODAY dates
    START = "2015-01-01"
    TODAY = date.today().strftime("%Y-%m-%d")

    # Retrieve NASDAQ-100 tickers
    url = "https://en.wikipedia.org/wiki/NASDAQ-100"
    nasdaq100_tickers = pd.read_html(url)[4]
    stock_ticker_list = nasdaq100_tickers['Ticker'].tolist()

    # Display stock list

    st.title("🌦️ Stock Forecast")
    # Select stock
    colss = st.columns([2, 1, 4])
    with colss[0].container():
        stock = st.selectbox("SELECT A STOCK", stock_ticker_list)
        stock_ticker = yf.Ticker(stock)
        stock_name = stock_ticker.info["longName"]
        with colss[2].expander(":green[**See Stock List**] 📈 "):
            st.dataframe(data=nasdaq100_tickers, use_container_width=True)

    # Years of prediction
    n_years = st.slider('Years of prediction:', 1, 5)
    period = n_years * 365

    # Load data function
    # @st.cache_data
    def load_data(ticker):
        try:
            data = yf.download(ticker, START, TODAY)
            data.reset_index(inplace=True)
            return data
        except Exception as e:
            st.error(f"Failed to fetch data for {ticker}. Error: {str(e)}")
            return None

    # Display raw data
    st.title("🗃️ Raw Data")
    data = load_data(stock)
    if data is not None:
        st.dataframe(data.tail(), use_container_width=True )
        # Plot raw data
        def plot_raw_data():
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
            fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
            fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
            st.plotly_chart(fig, use_container_width=True )
        plot_raw_data()

        # Forecast data
        st.title("🔎 Forecast Data ")
        @st.cache_resource
        def predict_forecast(df_train, period):
            m = Prophet()
            m.fit(df_train)
            future = m.make_future_dataframe(periods=period)
            forecast = m.predict(future)
            return m, forecast

        df_train = data[['Date', 'Close']]
        df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})
        m, forecast = predict_forecast(df_train, period)
        
        # Display forecast price
        st.write("Forecasted Close Price:")
        st.dataframe(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(), use_container_width=True )

        # Plot forecast
        st.write(f'Forecast plot for {n_years} years')
        fig1 = plot_plotly(m, forecast)
        st.plotly_chart(fig1, use_container_width=True )
