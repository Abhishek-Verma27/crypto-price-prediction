import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import pickle
import os


# Helper function to clean and convert monetary strings to numeric
def convert_to_numeric(value):
    try:
        value = value.replace("$", "").replace(",", "").strip()  # Remove $ and commas
        if "B" in value:
            return float(value.replace("B", "")) * 1e9  # Convert billions
        elif "M" in value:
            return float(value.replace("M", "")) * 1e6  # Convert millions
        else:
            return float(value)
    except Exception as e:
        return 0.0  # Default to 0 if conversion fails


# Load and preprocess the dataset
def load_data(file_path="data/crypto_data.csv"):
    # Load data
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dataset not found at {file_path}. Please ensure the file exists.")
    
    data = pd.read_csv(file_path)

    # Clean and convert columns
    data["market_cap"] = data["market_cap"].apply(convert_to_numeric)
    data["total_volume"] = data["total_volume"].apply(convert_to_numeric)
    data["current_price"] = data["current_price"].apply(convert_to_numeric)

    # Select relevant columns
    features = data[["market_cap", "total_volume"]]
    target = data["current_price"]

    return features, target


# Train the model
def train_model():
    features, target = load_data()

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

    # Train a Linear Regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"Model Performance:\nMean Squared Error: {mse:.2f}\nR-squared: {r2:.2f}")

    # Save the model
    model_path = "models/price_prediction_model.pkl"
    os.makedirs("models", exist_ok=True)
    with open(model_path, "wb") as f:
        pickle.dump(model, f)

    print(f"Model saved at {model_path}")


if __name__ == "__main__":
    train_model()
