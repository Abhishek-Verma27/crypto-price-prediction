import pandas as pd
import requests
import os

def fetch_from_coingecko():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": 100}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        print("Failed to fetch data from CoinGecko:", response.status_code)
        return pd.DataFrame()

def fetch_from_cryptocompare():
    api_key = "b514570b1394470b59371991f4ac5e96e4deecd71548be252ded2514e4c62482"  # Replace with your API key
    url = "https://min-api.cryptocompare.com/data/top/mktcapfull"
    params = {"limit": 100, "tsym": "USD", "api_key": api_key}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json().get("Data", [])
        records = []
        for item in data:
            coin = item.get("CoinInfo", {})
            display = item.get("DISPLAY", {}).get("USD", {})
            records.append({
                "symbol": coin.get("Name"),
                "market_cap": display.get("MKTCAP", "N/A"),
                "price": display.get("PRICE", "N/A"),
                "volume_24h": display.get("TOTALVOLUME24H", "N/A")
            })
        return pd.DataFrame(records)
    else:
        print("Failed to fetch data from CryptoCompare:", response.status_code)
        return pd.DataFrame()

def fetch_from_coinmarketcap():
    api_key = "0face062-7f0b-49cb-8122-ef5e8587fbe2"  # Replace with your API key
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    headers = {"X-CMC_PRO_API_KEY": api_key}
    params = {"start": "1", "limit": "100", "convert": "USD"}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json().get("data", [])
        records = []
        for item in data:
            records.append({
                "symbol": item.get("symbol"),
                "market_cap": item.get("quote", {}).get("USD", {}).get("market_cap", "N/A"),
                "price": item.get("quote", {}).get("USD", {}).get("price", "N/A"),
                "volume_24h": item.get("quote", {}).get("USD", {}).get("volume_24h", "N/A")
            })
        return pd.DataFrame(records)
    else:
        print("Failed to fetch data from CoinMarketCap:", response.status_code)
        return pd.DataFrame()

def fetch_crypto_data():
    # Ensure the 'data' directory exists
    os.makedirs("data", exist_ok=True)

    print("Fetching data from CoinGecko...")
    coingecko_data = fetch_from_coingecko()
    print("Fetching data from CryptoCompare...")
    cryptocompare_data = fetch_from_cryptocompare()
    print("Fetching data from CoinMarketCap...")
    coinmarketcap_data = fetch_from_coinmarketcap()

    # Combine all data into a single DataFrame
    combined_data = pd.concat([coingecko_data, cryptocompare_data, coinmarketcap_data], ignore_index=True)

    # Save to CSV
    combined_data.to_csv("data/crypto_data.csv", index=False)
    print("Data saved to data/crypto_data.csv")

if __name__ == "__main__":
    fetch_crypto_data()