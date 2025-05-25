import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import joblib

SEQUENCE_LENGTH = 60
DATA_PATH = "data"
MODEL_PATH = "models"
SCALER_PATH = "models"

def load_data(coin):
    file_path = os.path.join(DATA_PATH, f"{coin}_historical_data.csv")
    df = pd.read_csv(file_path, parse_dates=["time_period_start"])
    df = df.sort_values("time_period_start")
    return df

def load_model_and_scaler(coin):
    model = load_model(os.path.join(MODEL_PATH, f"{coin}_lstm_model.h5"), compile=False)
    scaler = joblib.load(os.path.join(SCALER_PATH, f"{coin}_lstm_scaler.pkl"))
    return model, scaler

def predict_future(model, scaler, data, predict_days=30):
    closing_prices = data["price_close"].values.reshape(-1, 1)
    scaled_data = scaler.transform(closing_prices)

    last_sequence = scaled_data[-SEQUENCE_LENGTH:].reshape(1, SEQUENCE_LENGTH, 1)
    predictions = []

    for _ in range(predict_days):
        pred = model.predict(last_sequence)[0][0]
        predictions.append(pred)

        last_sequence = np.append(last_sequence[:, 1:, :], [[[pred]]], axis=1)

    predicted_prices = scaler.inverse_transform(np.array(predictions).reshape(-1, 1))
    return predicted_prices

def visualize(data, predicted_prices, coin, predict_days):
    last_date = pd.to_datetime(data["time_period_start"].iloc[-1])
    future_dates = [last_date + pd.Timedelta(days=i+1) for i in range(predict_days)]

    plt.figure(figsize=(12, 6))
    plt.plot(data["time_period_start"], data["price_close"], label="Historical")
    plt.plot(future_dates, predicted_prices, label="Predicted", linestyle="--")
    plt.title(f"{coin} Price Prediction for Next {predict_days} Days")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{coin}_forecast_plot.png")
    plt.show()

def main(coin="BTC", predict_days=30):
    print(f"\n📈 Generating {predict_days}-day forecast for {coin}...\n")
    df = load_data(coin)
    model, scaler = load_model_and_scaler(coin)
    predicted_prices = predict_future(model, scaler, df, predict_days)

    for i, price in enumerate(predicted_prices):
        print(f"Day {i+1}: ${price[0]:,.2f}")

    visualize(df, predicted_prices, coin, predict_days)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--coin", type=str, default="BTC", choices=["BTC", "ETH"], help="Coin symbol")
    parser.add_argument("--days", type=int, default=30, help="Number of future days to predict")
    args = parser.parse_args()
    main(coin=args.coin, predict_days=args.days)
