import requests
import pandas as pd
import datetime
import os

API_KEY = '1b6bbacc-f951-4645-b3bb-a49274845546'
CHUNK_SIZE_DAYS = 30

def fetch_historical_data(symbol, period_id, api_key, start_date, end_date):
    url = f"https://rest.coinapi.io/v1/ohlcv/{symbol}/history?period_id={period_id}&time_start={start_date}T00:00:00&time_end={end_date}T23:59:59"
    headers = {"X-CoinAPI-Key": api_key}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data:
            df = pd.DataFrame(data)
            return df
        else:
            print(f"No data returned for {symbol} from {start_date} to {end_date}")
            return None
    else:
        print(f"Failed to fetch data for {symbol}. Status code: {response.status_code}")
        return None

def append_data_to_csv(df, filename):
    if os.path.isfile(filename):
        existing_df = pd.read_csv(filename)
        combined_df = pd.concat([existing_df, df])
        combined_df.drop_duplicates(subset=['time_period_start'], inplace=True)
        combined_df.sort_values('time_period_start', inplace=True)
        combined_df.to_csv(filename, index=False)
    else:
        df.to_csv(filename, index=False)

def fetch_data_in_chunks(symbol, period_id, api_key, start_date, end_date, chunk_size_days=30):
    current_start_date = start_date
    while current_start_date < end_date:
        next_end_date = (datetime.datetime.strptime(current_start_date, "%Y-%m-%d") + datetime.timedelta(days=chunk_size_days)).strftime("%Y-%m-%d")
        if next_end_date > end_date:
            next_end_date = end_date
        
        print(f"Fetching data for {symbol} from {current_start_date} to {next_end_date}")
        df = fetch_historical_data(symbol, period_id, api_key, current_start_date, next_end_date)
        if df is not None:
            append_data_to_csv(df, f"{symbol}_historical_data.csv")
        current_start_date = (datetime.datetime.strptime(next_end_date, "%Y-%m-%d") + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

def update_symbol_data(symbol, period_id="1DAY"):
    filename = f"{symbol}_historical_data.csv"
    if os.path.isfile(filename):
        existing_df = pd.read_csv(filename)
        existing_df['time_period_start'] = pd.to_datetime(existing_df['time_period_start'])
        last_date = existing_df['time_period_start'].max().strftime("%Y-%m-%d")
        start_date = (datetime.datetime.strptime(last_date, "%Y-%m-%d") + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    else:
        # If no file, start from a default date
        start_date = "2023-01-01"
    end_date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    if start_date > end_date:
        print(f"No new data to fetch for {symbol}. Latest data is up to date.")
        return
    
    fetch_data_in_chunks(symbol, period_id, API_KEY, start_date, end_date, CHUNK_SIZE_DAYS)

if __name__ == "__main__":
    # Update BTC data
    update_symbol_data("BTC")
    
    # Update ETH data
    update_symbol_data("ETH")
