import pandas as pd
import numpy as np

def preprocess_data():
    # Load the raw data
    data = pd.read_csv("data/crypto_data.csv")

    # Debugging: Display raw data sample
    print("Raw Data Sample:")
    print(data.head())

    # Check for missing columns and add default values
    required_columns = ["historical_trends", "sentiment_score", "macroeconomic_indicator"]
    for col in required_columns:
        if col not in data.columns:
            print(f"Column '{col}' missing. Adding default values.")
            if col == "historical_trends":
                data[col] = np.random.uniform(10000, 50000, len(data))  # Placeholder historical trend data
            elif col == "sentiment_score":
                data[col] = 0.5  # Neutral sentiment as default
            elif col == "macroeconomic_indicator":
                data[col] = 1.0  # Placeholder macroeconomic data

    # Convert columns to numeric, coercing errors to NaN
    data["current_price"] = pd.to_numeric(data["current_price"], errors='coerce')
    data["market_cap"] = pd.to_numeric(data["market_cap"], errors='coerce')
    data["volume_24h"] = pd.to_numeric(data["volume_24h"], errors='coerce')

    # Fill missing values in key columns with realistic defaults
    data["current_price"].fillna(1000, inplace=True)  # Replace NaN with default price
    data["market_cap"].fillna(1e9, inplace=True)      # Replace NaN with default market cap
    data["volume_24h"].fillna(1e7, inplace=True)      # Replace NaN with default volume

    # Remove rows with NaN or zero in the critical columns
    data = data[(data["current_price"] > 0) & (data["market_cap"] > 0) & (data["volume_24h"] > 0)]

    # Debugging: Display cleaned data
    print("Cleaned Data Sample:")
    print(data.head())
    print("Target Variable Stats:")
    print(data["current_price"].describe())

    # Save preprocessed data
    data.to_csv("data/preprocessed_data.csv", index=False)
    print("Preprocessed data saved to data/preprocessed_data.csv")

if __name__ == "__main__":
    preprocess_data()
