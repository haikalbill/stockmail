import streamlit as st
import yfinance as yf
import pandas as pd
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sn
import matplotlib.pyplot as plt
import base64
import io
from io import BytesIO
import os
from forex_python.converter import CurrencyRates
import requests
from datetime import datetime, timedelta
import math
import time
from functools import partial
import asyncio        
from money import Money
import requests
from PIL import Image
import forecast

def main():
    ##stock ticker list##
    url = "https://en.wikipedia.org/wiki/NASDAQ-100"
    nasdaq100_tickers = pd.read_html(url)[4]
    stock_list = nasdaq100_tickers
    stock_ticker_list = nasdaq100_tickers['Ticker'].tolist()
    ##st.write(stock_list)
    st.divider()
    #stocklistmarkdown =st.markdown("*Streamlit* is **really** ***cool***.")


    ##topstock## 
    def get_stock_data(tickers):
        data = {}
        for ticker in tickers:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="1d")
            if not hist.empty:
                data[ticker] = hist.iloc[0]
        return pd.DataFrame(data).T

    top_stock = get_stock_data(stock_ticker_list)
    top_stock = top_stock.reset_index().rename(columns={'index': 'Ticker'})
    # Adding a selectbox for sorting criterion
    colss = st.columns([2,11])
    sort_by = colss[0].selectbox('Sort stocks by:', ('Most Expensive', 'Least Expensive', 'Most Active', 'Least Active'))
    
    if not top_stock.empty:
        # Merging stock list with stock data to include names
        merged_data = pd.merge(stock_list, top_stock, left_on='Ticker', right_on='Ticker', how='left')

        # Determine the sorting parameters
        if sort_by == 'Most Expensive':
            sorted_data = merged_data.sort_values(by='Close', ascending=False)
        elif sort_by == 'Least Expensive':
            sorted_data = merged_data.sort_values(by='Close', ascending=True)
        elif sort_by == 'Most Active':
            sorted_data = merged_data.sort_values(by='Volume', ascending=False)
        elif sort_by == 'Least Active':
            sorted_data = merged_data.sort_values(by='Volume', ascending=True)
        
        # Select top 5 stocks based on sorting
        top_5_stocks = sorted_data[['Ticker', 'Company', 'Open', 'High', 'Low', 'Close', 'Volume']].head(5)
        
        # Ensure we have exactly 5 columns, even if fewer than 5 stocks are available
        num_stocks = len(top_5_stocks)
        cols = st.columns(5)
        for idx in range(5):
            if idx < num_stocks:
                row = top_5_stocks.iloc[idx]
                with cols[idx]:
                    st.metric(
                        label=f"{row['Company']} ({row['Ticker']})",
                        value=f"${row['Close']:.2f}",
                        delta=f"Volume: {row['Volume']}"
                    )
            else:
                # Placeholder for empty columns
                with cols[idx]:
                    st.write("No data")
    else:
        st.write('No data available.')
    st.divider()
    ##stockselection##
    colss = st.columns([3,1,7])
    with colss[0].container():
        #cols = st.columns([1, 1, 1])
        
        stock = st.selectbox("Select a Stock", stock_ticker_list)
        stock_ticker = yf.Ticker(stock)
        stock_name = stock_ticker.info["longName"]


    ##timeframe##
        default_start_date = datetime.today() - timedelta(weeks=52)
        cols = st.columns([2, 2])
        start_date = cols[0].date_input("Start Date", default_start_date)
        end_date = cols[1].date_input("End Date")
        hist = stock_ticker.history(period="1mo")
        #st.markdown("![Alt](https://media.giphy.com/media/Xf1ghvcjLrMn3O6Qe4/giphy.gif)")
        #colss[0].markdown("![Alt Text](https://media.giphy.com/media/TLayDh2IZOHPW/giphy.gif)")
    with colss[2].container():        
        with st.expander(":green[**See Stock List**] 📈 "):
            st.dataframe(data=stock_list, use_container_width=True)

            
    st.divider()
    stock_ticker = yf.Ticker(stock)

    #st.write(stock_ticker.recommendations)
    #st.write(stock_ticker.recommendations_summary)

    ###stock data###


    with st.container():
        collu = st.columns([2,3])
        current_price = stock_ticker.info["currentPrice"]
        previous_price = stock_ticker.info["previousClose"]
        current_percent = current_price / previous_price * 100 - 100
        #float(current_percent)
        new_current_percent = round(current_percent,3)
        #collu[0].markdown(gradient_text_html.format(stock_name), unsafe_allow_html=True)
        collu[0].title(f"{stock_name}")
        #collu[0].markdown(f"<h1 style='background: linear-gradient(to right, #073f6b, #61C2C6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>{stock_name}</h1>", unsafe_allow_html=True)
        if current_price < previous_price:
            collu[1].title(f"{current_price} 🔻:red[{new_current_percent}%]")
            #collu[1].markdown(f"<p style='font-weight: bold; text-align: inline; font-size: 34px;'>Current price: {current_price}<p style='font-weight: bold; text-align: inline; font-size: 20px;color:red'>{current_price}{new_current_percent}%", unsafe_allow_html=True)
        else:
            collu[1].title(f"{current_price} 🔺:green[{new_current_percent}%]")
            #collu[1].markdown(f"<p style='font-weight: bold; text-align: inline; font-size: 34px;'>Current price: {current_price} <p style='font-weight: bold; text-align: inline; font-size: 20px; color: green'>{new_current_percent}%", unsafe_allow_html=True)

        

    stock_data = yf.download(stock, start=start_date, end=end_date)
    #collu[1].metric(label="Current Prices", value= current_price, delta=new_current_percent)

    ##bar graph##
    st.title("📊 Stock Prices Graph")

    fig = go.Figure(data= go.Candlestick(x=stock_data.index,
                                        open=stock_data['Open'],
                                        high=stock_data['High'],
                                        low=stock_data['Low'],
                                        close=stock_data['Close']
                                        ))

    fig.update_layout(yaxis_title=f'Price',
                        xaxis_title='Date')

    st.plotly_chart(fig, use_container_width=True)

    #if st.button("Refresh Page"):
    #    st.experimental_rerun()

            
    ###stock table###

    st.title("🧾 Stock Prices Table")

    ##table alternative (other data type)##
    #stock_table = st.dataframe(hist)
    st.dataframe(stock_data ,use_container_width=True )
    st.divider()


    ##news##
    st.title(f'📰 Latest News on {stock_name} ')  

    def get_thumbnail(news_item, default_image_url):
        try:
            return news_item["thumbnail"]["resolutions"][0]["url"]
        except KeyError:
            return default_image_url
        
    def display_news_item(news_item):
        default_image_url = "https://i.ibb.co/chVqfCZ/1.png"  # Replace with your actual default image URL
        img_url = get_thumbnail(news_item, default_image_url)
        response = requests.get(img_url)
        img = Image.open(BytesIO(response.content))
        img.thumbnail((100, 100))  # Set width and height in pixels
        with st.container(height =170 ,border=True):
            newscol1, newscol2 = st.columns([1, 5])
            # newscol1.image(img,use_column_width=True)
            newscol2.info(news_item["title"])
            newscol1.link_button("Read News", news_item["link"])
            newscol2.warning(f'Published by ***{news_item["publisher"]}***')

    # Usage
    # newscoll1, newscoll2 = st.columns([1,1])
    # with newscoll1:
    #     for i in range(4):
    #         news_item = stock_ticker.news[i]
    #         display_news_item(news_item)

    # with newscoll2:
    #     for i in range(4, min(8, len(stock_ticker.news))):
    #         news_item = stock_ticker.news[i]
    #         display_news_item(news_item)
    
    try:
        if stock_ticker.news:
            newscoll1, newscoll2 = st.columns([1,1])
            with newscoll1:
                for i in range(4):
                    news_item = stock_ticker.news[i]
                    display_news_item(news_item)
    
            with newscoll2:
                for i in range(4, min(8, len(stock_ticker.news))):
                    news_item = stock_ticker.news[i]
                    display_news_item(news_item)
    except requests.exceptions.JSONDecodeError as e:
        st.write(f"An error occurred: {e}")
