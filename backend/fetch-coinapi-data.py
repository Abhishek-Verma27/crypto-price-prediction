import requests
import pandas as pd
import datetime
import os

def fetch_historical_data(symbol, period_id, api_key, start_date, end_date):
    url = f"https://rest.coinapi.io/v1/ohlcv/{symbol}/history?period_id={period_id}&time_start={start_date}&time_end={end_date}"
    headers = {"X-CoinAPI-Key": api_key}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
        return df
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None

def append_data_to_csv(df, filename):
    if os.path.isfile(filename):
        existing_df = pd.read_csv(filename)
        df = pd.concat([existing_df, df])
    df.to_csv(filename, index=False)

def fetch_data_in_chunks(symbol, period_id, api_key, start_date, end_date, chunk_size_days=30):
    current_start_date = start_date
    while current_start_date < end_date:
        current_end_date = (datetime.datetime.strptime(current_start_date, "%Y-%m-%d") + datetime.timedelta(days=chunk_size_days)).strftime("%Y-%m-%d")
        if current_end_date > end_date:
            current_end_date = end_date
        print(f"Fetching data from {current_start_date} to {current_end_date}")
        df = fetch_historical_data(symbol, period_id, api_key, current_start_date, current_end_date)
        if df is not None:
            append_data_to_csv(df, f"{symbol}_historical_data.csv")
        current_start_date = (datetime.datetime.strptime(current_end_date, "%Y-%m-%d") + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

# Replace 'YOUR_API_KEY' with your actual API key
api_key = '1b6bbacc-f951-4645-b3bb-a49274845546'

# Fetch historical data for Bitcoin (BTC/USD)
fetch_data_in_chunks("BITSTAMP_SPOT_BTC_USD", "1DAY", api_key, "2023-01-01", "2025-01-18")

# Fetch historical data for Ethereum (ETH/USD)
fetch_data_in_chunks("BITSTAMP_SPOT_ETH_USD", "1DAY", api_key, "2023-01-01", "2025-01-18")
