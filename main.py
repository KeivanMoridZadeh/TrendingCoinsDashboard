import io
import json
import time
import numpy as np
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from PIL import Image


sns.set_theme(style="darkgrid", context="talk")

# Constants
VS_CURRENCY = 'usd'
HEADERS = {"accept": "application/json"}
TRENDING_URL = "https://api.coingecko.com/api/v3/search/trending"
DAYS_REQUESTED = 30  


@st.cache_data(show_spinner=False)
def fetch_trending_data(url, headers, days_requested):
    
    coins = []
    response = requests.get(url, headers=headers)
    data = response.json()
    for i in range(5):
        coin_id = data["coins"][i]["item"]["id"]
        prices = fetch_coin_prices(coin_id, days_requested)
        if prices:
            coin_entry = {
                "name": data["coins"][i]["item"]["name"],
                "coin_id": coin_id,
                "symbol": data["coins"][i]["item"]["symbol"],
                "price": prices,
            }
            coins.append(coin_entry)
    return coins

@st.cache_data(show_spinner=False)
def fetch_coin_prices(coin_id, days):
  
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/ohlc"
    params = {"vs_currency": VS_CURRENCY, "days": str(days)}
    response = requests.get(url, headers=HEADERS, params=params)
    data = response.json()
    
    
    if isinstance(data, list) and len(data) > 0:
        high_prices = [candle[2] for candle in data]
        if max(high_prices) < 0.0001:
            time.sleep(5)
            return []
        #i used time.sleep(5) for this part to not get rate limite error
        time.sleep(5)
        if len(high_prices) >= days:
            return high_prices[-days:]
        else:
            missing = days - len(high_prices)
            return [np.nan] * missing + high_prices
    else:
        time.sleep(5)
        st.error(f"Error")
        return []

def create_price_plot(coins_data, days_requested):

    plt.figure(figsize=(12, 8))
    for coin in coins_data:
        prices = coin["price"]
        if not prices:
            continue
    
        if len(prices) >= days_requested:
            prices = prices[-days_requested:]
        else:
            missing = days_requested - len(prices)
            prices = [np.nan] * missing + prices
        x = list(range(1, days_requested + 1))
        plt.plot(x, prices, marker='o', linewidth=2, markersize=6, label=coin["name"])
    plt.xlabel("Day (Last 30 Days)", fontsize=14)
    plt.ylabel("Highest Price (USD)", fontsize=14)
    plt.title("Trending Coins: Daily Highest Prices Over Last 30 Days", fontsize=16)
    plt.xticks(list(range(1, days_requested + 1)))
    handles, labels = plt.gca().get_legend_handles_labels()
    if handles:
        plt.legend(fontsize=12)
    plt.tight_layout()
    
    # Save the plot to an in-memory buffer
    # I used AI for this part :) Not my code!
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()
    return buf


st.title("Trending Coins Dashboard (30 Days)")

# Button to fetch data and plot
if st.button("Fetch Data and Plot"):
    with st.spinner("Fetching trending coin data..."):
        coins_data = fetch_trending_data(TRENDING_URL, HEADERS, DAYS_REQUESTED)
    st.write("Coin Data:")
    st.json(coins_data)
    
    # Generate the plot and display it
    plot_buffer = create_price_plot(coins_data, DAYS_REQUESTED)
    image = Image.open(plot_buffer)
    st.image(image, caption="Daily Highest Prices", use_container_width=True)
