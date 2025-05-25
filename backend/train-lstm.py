import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, r2_score
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import EarlyStopping, CSVLogger
import joblib
import os
import logging
from tqdm import tqdm

# Set up logging to file and console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("training.log"),
        logging.StreamHandler()
    ]
)

# Create models directory if missing
os.makedirs("models", exist_ok=True)

def create_sequences(data, sequence_length):
    X, y = [], []
    # tqdm progress bar for sequence creation
    for i in tqdm(range(len(data) - sequence_length), desc="Creating sequences"):
        X.append(data[i:i + sequence_length])
        y.append(data[i + sequence_length])
    return np.array(X), np.array(y)

def train_lstm_model(csv_path, crypto_type, sequence_length=30):
    logging.info(f"Starting training for {crypto_type}")

    # Load data
    df = pd.read_csv(csv_path)
    logging.info(f"Loaded {len(df)} rows from {csv_path}")

    prices = df[['price_close']].copy()

    # Scale prices
    scaler = MinMaxScaler()
    scaled_prices = scaler.fit_transform(prices)
    logging.info(f"Data scaled with MinMaxScaler")

    # Create sequences for LSTM input
    X, y = create_sequences(scaled_prices, sequence_length)
    logging.info(f"Created {len(X)} sequences of length {sequence_length}")

    # Train/test split (80/20)
    split_idx = int(0.8 * len(X))
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]
    logging.info(f"Split data: {len(X_train)} train, {len(X_test)} test")

    # Build smaller LSTM model to fit system capacity
    model = Sequential([
        LSTM(32, activation='relu', input_shape=(sequence_length, 1)),  # 32 units to save memory
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    logging.info("Model compiled")

    # Callbacks: early stopping + CSV logger for epoch progress
    es = EarlyStopping(patience=3, restore_best_weights=True)
    csv_logger = CSVLogger(f'training_{crypto_type}.csv')

    batch_size = 16  # Smaller batch size for GPU memory constraints
    epochs = 30

    logging.info(f"Starting model.fit with batch_size={batch_size}, epochs={epochs}")

    # Fit model with progress output (verbose=2)
    history = model.fit(
        X_train, y_train,
        epochs=epochs,
        batch_size=batch_size,
        validation_split=0.1,
        callbacks=[es, csv_logger],
        verbose=2
    )

    logging.info(f"Training completed for {crypto_type}")

    # Predict and invert scaling for evaluation
    y_pred = model.predict(X_test)
    y_test_inv = scaler.inverse_transform(y_test)
    y_pred_inv = scaler.inverse_transform(y_pred)

    mse = mean_squared_error(y_test_inv, y_pred_inv)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test_inv, y_pred_inv)

    logging.info(f"{crypto_type} evaluation metrics:")
    logging.info(f"  MSE:  {mse:.4f}")
    logging.info(f"  RMSE: {rmse:.4f}")
    logging.info(f"  R²:   {r2:.4f}")

    # Save model and scaler
    model_path = f"models/{crypto_type}_lstm_model.h5"
    scaler_path = f"models/{crypto_type}_lstm_scaler.pkl"
    model.save(model_path)
    joblib.dump(scaler, scaler_path)
    logging.info(f"Saved model to {model_path}")
    logging.info(f"Saved scaler to {scaler_path}")

if __name__ == "__main__":
    train_lstm_model("data/BTC_historical_data.csv", "BTC")
    train_lstm_model("data/ETH_historical_data.csv", "ETH")