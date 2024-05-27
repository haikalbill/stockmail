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
import stockmail
import welcome
from dateutil.parser import parse


def main():

    column = st.columns([9,1])
    # Outlier warning
    column[0].warning("""
        **Stockmail** is an open-source stock data created to help any new traders to obtain sufficient and latest data on stock market
        in order to make the best decision regarding the stock trading. 
    """)

    # Title
    column[0].title('📊 Stockmail Dashboard')


    # Introduction
    column[0].info(
        """
        The stock market continues to progress and its development has never stopped.
        Analysts and investors keep developing each segment of the industry and the whole stock market ecosystem.
        This tool, the StockMail Dashboard, is designed to allow viewers to journey into the world of stock ecosystems of some of the major companies,
        and compare their performance.

        The StockMail Dashboard is structured in multiple Pages that are accessible using the sidebar. Each of these Pages addresses a different segment of the stock market.
        Within each segment, you are able to filter your desired companies to narrow/expand the comparison.
        By selecting a single company, you can observe a deep dive into that particular network.

        The dashboard provides stock data information with graphs and news regarding the stock and company. It also includes a table for new users to analyze various metrics.
        Additionally, the StockMail Dashboard offers stock forecasts for up to 5 years, allowing users to make informed decisions based on predicted trends.
        
        All values for amounts, prices, and volumes are in U.S. dollars, however we provide a currency exchange for users to use in order to change the their desired currency.
        """
    )
    
