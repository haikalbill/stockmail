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
import random
import time
from functools import partial
import asyncio        
from money import Money
import requests
from PIL import Image
import forecast
import stockmail
import welcome
from dateutil.parser import parse


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

logocol1, logocol2 = st.columns([1, 6])
logo2 = "https://i.ibb.co/PNPWVmv/4-removebg-preview.png"
logo1 = "https://i.ibb.co/r7xKkT5/2-removebg-preview-2.png"
logocol1.image(logo1)
logocol2.markdown(gradient_text_html, unsafe_allow_html=True)
logocol2.markdown("<p style='font-weight: bold; text-align: inline; font-size: 20px;'>The goal of succesful trader is to make the best trades. Money is secondary</p>", unsafe_allow_html=True)
# Create a placeholder for the clock
clock_placeholder = st.empty()
current_time = datetime.now().strftime("%H:%M:%S")
#clock_placeholder.write(f"**Current Time: {current_time}**")


############################################################################################################################################
 ##sidebar##
 
 ##navigation##
# Define a function for each page

def page_welcome():
    welcome.main()
    
def page_forecast():
    forecast.main()

def page_stockmail():
    stockmail.main()

# Create a dictionary of pages
pages = {
    '🏠 Home': page_welcome,
    '📊 Stockmail': page_stockmail,
    '🌦️ Stock Forecast': page_forecast
}

# Add a selectbox to the sidebar for navigation
st.sidebar.markdown("<p style='font-weight: bold; text-align: inline; font-size: 20px;'>🚩 NAVIGATION </p>", unsafe_allow_html=True)
selection = st.sidebar.radio('Go to', list(pages.keys()))
st.sidebar.divider()
st.sidebar.markdown("<p style='font-weight: bold; text-align: inline; font-size: 20px;'>🔄 CURRENCY EXCHANGE </p>", unsafe_allow_html=True)
#st.sidebar.markdown("![Alt Text](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExem44aXVwYjFrMmU5bnN3ZnIxcThsc292bGxsOWtuaTFtdzZjYWRhYiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/YnkMcHgNIMW4Yfmjxr/giphy.gif)")


##moneychanging##
# Input fields

amount = st.sidebar.number_input('Enter amount', min_value=0.01, step=0.01)
from_currency = st.sidebar.selectbox('From Currency', options=["USD","MYR", "EUR", "JPY", "GBP", "AUD", "CAD", "CHF", "CNY", "SEK", "NZD"])
to_currency = st.sidebar.selectbox('To Currency', options=["USD","MYR", "EUR", "JPY", "GBP", "AUD", "CAD", "CHF", "CNY", "SEK", "NZD"])

# Currency conversion
if st.sidebar.button('Convert'):
    url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
    response = requests.get(url)
    data = response.json()
    conversion_rate = data['rates'][to_currency]
    converted_amount = amount * conversion_rate
    st.sidebar.info(f'***{amount} {from_currency}***  is equivalent to  ***{converted_amount:.2f} {to_currency}***')


# Create a list of spinner messages
spinner_messages = [
    'Please wait while the intern refills his coffee...',
    'Web developers do it with <style>...',
    'Spinning up the hamster wheel...',
    'Spinning the wheel of fortune...',
    'Shoveling coal into the server...',
    'Programming the flux capacitor...'
]

# Choose a random spinner message
spinner_message = random.choice(spinner_messages)

# Display the selected page with the session state
with st.spinner(spinner_message):
    time.sleep(5)
    pages[selection]()

#pages[selection]()


# for i in range(5):
#     news_item = stock_ticker.news[i]
#     img = get_thumbnail(news_item, default_image_url)
#     with col1:
#         with st.container(border=True):
#             newscol1, newscol2 = st.columns([2, 5])
#             newscol1.image(img, use_column_width=True)
#             news_title = news_item["title"]
#             newscol2.write(news_title)
#             newscol2.link_button("Read News", news_item["link"])
#             newscol2.write(f'Published by "{news_item["publisher"]}"')

# news_publisher1 = stock_ticker.news[0]["publisher"]
# news_publisher2 = stock_ticker.news[1]["publisher"]
# news_publisher3 = stock_ticker.news[2]["publisher"]
# news_publisher4 = stock_ticker.news[3]["publisher"]
# news_publisher5 = stock_ticker.news[4]["publisher"]
# img1 = stock_ticker.news[1]["thumbnail"]["resolutions"][0]["url"]
# st.image(img1, use_column_width=True)



# with col1:
#     with st.container(border = True):
#         newscol1,newscol2 = st.columns([2,5])
#         newscol1.image(img1, use_column_width=True)
#         news_title = stock_ticker.news[0]["title"]
#         newscol2.write(news_title)
#         newscol2.link_button("Read News", stock_ticker.news[0]["link"])
#         newscol2.write(f'Publised by "{news_publisher1}"')   

#     with st.container(border = True):
#         stock_ticker.news[1]["title"]
#         st.link_button("Read News", stock_ticker.news[1]["link"]) 
#         st.write(f'Publised by "{news_publisher2}"')   
        
#     with st.container(border = True):
#         stock_ticker.news[2]["title"]
#         st.link_button("Read News", stock_ticker.news[2]["link"])
#         st.write(f'Publised by "{news_publisher3}"')   

#     with st.container(border = True):
#         stock_ticker.news[3]["title"]
#         st.link_button("Read News", stock_ticker.news[3]["link"])
#         st.write(f'Publised by "{news_publisher4}"') 
        
#     with st.container(border = True):
#         stock_ticker.news[4]["title"]
#         st.link_button("Read News", stock_ticker.news[4]["link"])
#         st.write(f'Publised by "{news_publisher5}"') 

# with col2:
#     st.markdown("![Alt Text](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExem44aXVwYjFrMmU5bnN3ZnIxcThsc292bGxsOWtuaTFtdzZjYWRhYiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/YnkMcHgNIMW4Yfmjxr/giphy.gif)")
# #    stock_ticker.info
# #    stock_ticker.news
# img1 = stock_ticker.news[1]["thumbnail"]["resolutions"][0]["url"]
# st.write(img1)
# image_url = "https://s.yimg.com/uu/api/res/1.2/UfNPsRi0m54aItY_qLFDbg--~B/Zmk9ZmlsbDtoPTE0MDtweW9mZj0wO3c9MTQwO2FwcGlkPXl0YWNoeW9u/https://media.zenfs.com/en/zacks.com/46ebfcbff417ac1bbde85ad33fa0d4be"
# st.image(img1, use_column_width=True)


# # Sidebar with real-time clock
# st.sidebar.header("Real-Time Clock")

# # Placeholder for the clock
# clock_placeholder = st.sidebar.empty()

# while True:
#     # Get the current time
#     now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
#     # Update the clock in the sidebar
#     clock_placeholder.markdown(f"**{now}**")
    
#     # Sleep for 1 second before updating the time again
#     #time.sleep(1)

