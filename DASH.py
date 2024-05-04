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
import os
from forex_python.converter import CurrencyRates
import requests
from datetime import datetime, timedelta
import math


st.set_page_config(page_title="Stockmail",
                   page_icon=" :bar_chart",
                   layout= "wide"
                   )
##page layout##
gradient_text_html = """
<style>
.gradient-text {
    font-weight: bold;
    background: -webkit-linear-gradient(left, red, orange);
    background: linear-gradient(to right, red, orange);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    display: inline;
    font-size: 5em;
    text-align: center;
}
</style>
<div class="gradient-text">STOCKMAIL</div>
"""

st.markdown(gradient_text_html, unsafe_allow_html=True)
st.markdown("<p style='font-weight: bold; text-align: inline; font-size: 20px;'>The goal of succesful trader is to make the best trades. Money is secondary</p>", unsafe_allow_html=True)


############################################################################################################################################
##sidebar##
sidebar_title = ''':rainbow[MONEY CHANGER] 💸🔄💰.'''
st.sidebar.header(sidebar_title)

##moneychanging##
amount = st.sidebar.number_input('Enter amount to convert', min_value=0.01, step=0.01)

from_currency = st.sidebar.selectbox('From Currency', options=["USD", "EUR", "JPY", "GBP", "AUD", "CAD", "CHF", "CNY", "SEK", "NZD",
    "MXN", "SGD", "HKD", "NOK", "KRW", "TRY", "RUB", "INR", "BRL", "ZAR",
    "SAR", "AED", "PLN", "THB", "IDR", "DKK", "MYR", "HUF", "CZK", "ILS",
    "CLP", "PHP", "COP", "TWD", "ARS", "VND", "EGP", "KWD", "QAR", "NGN",
    "BDT", "RON", "PKR", "IQD", "CUC", "OMR", "CUP", "JOD", "BHD", "DZD",
    "TND", "MAD", "PEN", "LKR", "UAH", "XOF", "UGX", "BYN", "XAF", "TZS",
    "GHS", "RSD", "SYP", "AOA", "UGX", "KES", "MZN", "XPF", "VUV", "HTG",
    "PYG", "BIF", "GMD", "KYD", "MVR", "LSL", "MWK", "NAD", "SCR", "SLL",
    "SZL", "TOP", "XCD", "AFN", "ALL", "AMD", "ANG", "AOA", "ARS", "AUD",
    "AWG", "AZN", "BAM", "BBD", "BDT", "BGN", "BHD", "BIF", "BMD", "BND",
    "BOB", "BRL", "BSD", "BTN", "BWP", "BYN", "BZD", "CAD", "CDF", "CHF",
    "CLP", "CNY", "COP", "CRC", "CUC", "CUP", "CVE", "CZK", "DJF", "DKK",
    "DOP", "DZD", "EGP", "ERN", "ETB", "EUR", "FJD", "FKP", "GBP", "GEL",
    "GGP", "GHS", "GIP", "GMD", "GNF", "GTQ", "GYD", "HKD", "HNL", "HRK",
    "HTG", "HUF", "IDR", "ILS", "IMP", "INR", "IQD", "IRR", "ISK", "JEP",
    "JMD", "JOD", "JPY", "KES", "KGS", "KHR", "KMF", "KPW", "KRW", "KWD",
    "KYD", "KZT", "LAK", "LBP", "LKR", "LRD", "LSL", "LYD", "MAD", "MDL",
    "MGA", "MKD", "MMK", "MNT", "MOP", "MRU", "MUR", "MVR", "MWK", "MXN",
    "MYR", "MZN", "NAD", "NGN", "NIO", "NOK", "NPR", "NZD", "OMR", "PAB",
    "PEN", "PGK", "PHP", "PKR", "PLN", "PYG", "QAR", "RON", "RSD", "RUB",
    "RWF", "SAR", "SBD", "SCR", "SDG", "SEK", "SGD", "SHP", "SLL", "SOS",
    "SRD", "SSP", "STN", "SVC", "SYP", "SZL", "THB", "TJS", "TMT", "TND",
    "TOP", "TRY", "TTD", "TWD", "TZS", "UAH", "UGX", "USD", "UYU", "UZS",
    "VES", "VND", "VUV", "WST", "XAF", "XCD", "XDR", "XOF", "XPF", "ZAR"])
to_currency = st.sidebar.selectbox('To Currency', options=['USD', 'EUR', 'GBP', 'JPY','MYR'])
############################################################################################################################################

#Convert currency#
if st.sidebar.button('Convert'):
    c = CurrencyRates()
    rate = c.get_rate(from_currency, to_currency)
    converted_amount = amount * rate
    st.sidebar.write(f'{amount} {from_currency} is equivalent to {converted_amount:.2f} {to_currency}')



##stock ticker list##
url = "https://en.wikipedia.org/wiki/NASDAQ-100"
nasdaq100_tickers = pd.read_html(url)[4]
stock_list = nasdaq100_tickers
stock_ticker_list = nasdaq100_tickers['Ticker'].tolist()
##st.write(stock_list)
st.divider()


##stockselection##
colss = st.columns([2,1,4])
with colss[0].container():
    #cols = st.columns([1, 1, 1])
    stock = st.selectbox("SELECT A STOCK", stock_ticker_list)
    stock_ticker = yf.Ticker(stock)
    stock_name = stock_ticker.info["longName"]

##timeframe##
    default_start_date = datetime.today() - timedelta(weeks=52)
    cols = st.columns([2, 2])
    start_date = cols[0].date_input("Start Date", default_start_date)
    end_date = cols[1].date_input("End Date")
    hist = stock_ticker.history(period="1mo")
    st.markdown("![Alt Text](https://media.giphy.com/media/TLayDh2IZOHPW/giphy.gif)")

    
    colss[2].write(stock_list)

st.divider()
stock_ticker = yf.Ticker(stock)

###stock data###
with st.container():
    collu = st.columns([2,3])
    current_price = stock_ticker.info["currentPrice"]
    previous_price = stock_ticker.info["previousClose"]
    current_percent = current_price / previous_price * 100 - 100
    #float(current_percent)
    new_current_percent = round(current_percent,3)
    collu[0].title(f":blue[{stock_name}]")
    if current_price < previous_price:
        collu[1].title(f"{current_price}  🔻:red[{new_current_percent}%]")
    else:
        collu[1].title(f"{current_price}  🔺:green[{new_current_percent}%]")
           
###stock table###
with st.container():
    cols = st.columns([5,5,2])
    cols[0].header(" Stock Prices Table")
    stock_data = yf.download(stock, start=start_date, end=end_date)
    cols[0].write(stock_data)
    ##table alternative (other data type)##
    #stock_table = st.dataframe(hist)
    
##bar graph##
    cols[1].header("Stock Prices Graph")
    fig = go.Figure(data= go.Candlestick(x=stock_data.index,
                                        open=stock_data['Open'],
                                        high=stock_data['High'],
                                        low=stock_data['Low'],
                                        close=stock_data['Close']))

    fig.update_layout(yaxis_title=f'Price',
                        xaxis_title='Date')

    cols[1].plotly_chart(fig)

clicked = st.button('Hit me')
if clicked:
    print('Button clicked!')


##collumn##    
col1, col2 = st.columns(2)
col2.write('Column 1')
col1.title('LATEST NEWS ON THE COMPANY')  
  
##news##
news_publisher1 = stock_ticker.news[0]["publisher"]
news_publisher2 = stock_ticker.news[1]["publisher"]
news_publisher3 = stock_ticker.news[2]["publisher"]
 
with col1:
    with st.container(border = True):
        stock_ticker.news[0]["title"]
        stock_ticker.news[0]["link"]
        st.write(f'Publised by "{news_publisher1}"')   

    with st.container(border = True):
        stock_ticker.news[1]["title"]
        stock_ticker.news[1]["link"] 
        st.write(f'Publised by "{news_publisher2}"')   
        
    with st.container(border = True):
        stock_ticker.news[2]["title"]
        stock_ticker.news[2]["link"]
        st.write(f'Publised by "{news_publisher3}"')   


with col2:
    stock_ticker.info
    stock_ticker.news
