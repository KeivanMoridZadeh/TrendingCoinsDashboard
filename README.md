Trending Coins Dashboard (30 Days)
Trending Coins Dashboard is a fun and interactive web app I built using Python and Streamlit. It fetches trending cryptocurrency data from the CoinGecko API and displays a neat 30-day graph showing the daily highest prices for the top trending coins. This project is a great example of my skills in API integration, data visualization with Matplotlib/Seaborn, and building interactive web UIs with Streamlit.

What It Does
Fetches Trending Data:
It retrieves trending coin data (the first 5 coins) from the CoinGecko API.

Retrieves 30 Days of Prices:
For each coin, the app gets 30 days of OHLC (Open, High, Low, Close) data and extracts the highest price of each day.

Generates a Graph:
It creates a clear, visually appealing line graph using Matplotlib and Seaborn, showing daily highest prices over the last 30 days.

Displays Data on the Web:
The coin data (in JSON format) and the graph are displayed on a simple, clean web UI built with Streamlit.

Technologies Used
Python 3 – The programming language used.
Streamlit – For the web interface.
Matplotlib & Seaborn – For creating and styling the graph.
CoinGecko API – To fetch trending cryptocurrency data.
Pillow – For image processing (displaying the graph).
