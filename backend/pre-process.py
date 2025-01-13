import pandas as pd
from sklearn.preprocessing import StandardScaler

def preprocess_data(input_path="data/crypto_data.csv", output_path="data/processed_data.csv"):
    # Load the data
    data = pd.read_csv(input_path)

    # Display columns to understand structure
    print("Columns in data:", data.columns)

    # Keep only relevant columns
    relevant_columns = ["market_cap", "price", "volume_24h"]  # Adjust based on the dataset
    data = data[relevant_columns]

    # Drop rows with missing or non-numeric values
    data = data.dropna()
    data = data.apply(pd.to_numeric, errors="coerce").dropna()

    # Normalize the data
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data)
    processed_data = pd.DataFrame(scaled_data, columns=relevant_columns)

    # Save the processed data
    processed_data.to_csv(output_path, index=False)
    print(f"Processed data saved to {output_path}")

if __name__ == "__main__":
    preprocess_data()
