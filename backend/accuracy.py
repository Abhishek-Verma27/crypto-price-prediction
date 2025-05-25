import os
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score
import tensorflow as tf
from sklearn.preprocessing import StandardScaler

# Paths
models_dir = r"C:\Users\abhis\OneDrive\Desktop\crypto-price-prediction\backend\models"  # Change this to your models folder
test_data_paths = {
    "Dataset 1": r"C:\Users\abhis\OneDrive\Desktop\crypto-price-prediction\backend\data\preprocessed_btc_data.csv",  # Update paths
    "Dataset 2": r"C:\Users\abhis\OneDrive\Desktop\crypto-price-prediction\backend\data\preprocessed_eth_data.csv"
}

# Features used for prediction
FEATURES = ['lag_1', 'lag_2', 'lag_3', 'lag_4', 'lag_5']
TARGET = 'price_close'

# Function to load and preprocess dataset
def load_and_preprocess_data(file_path):
    df = pd.read_csv(file_path)
    X = df[FEATURES]
    y = df[TARGET]

    # Standardize features using the same scaler used during training
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    return X_scaled, y

# Function to evaluate models
def evaluate_models(models_dir, dataset_name, X_test, y_test):
    results = []

    for model_file in os.listdir(models_dir):
        model_path = os.path.join(models_dir, model_file)

        try:
            if model_file.endswith(".pkl") or model_file.endswith(".joblib"):
                model = joblib.load(model_path)
                y_pred = model.predict(X_test)

            elif model_file.endswith(".h5"):
                model = tf.keras.models.load_model(model_path)
                y_pred = model.predict(X_test).flatten()  # Ensure correct output shape

            else:
                print(f"Skipping unsupported model format: {model_file}")
                continue

            # Compute evaluation metrics
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)

            results.append((dataset_name, model_file, mse, r2))

        except Exception as e:
            print(f"Error evaluating {model_file}: {e}")

    return results

# Run evaluation
all_results = []
for dataset_name, test_data_path in test_data_paths.items():
    X_test, y_test = load_and_preprocess_data(test_data_path)
    all_results.extend(evaluate_models(models_dir, dataset_name, X_test, y_test))

# Print results
print("Model Evaluation Results:")
print("{:<10} {:<30} {:<15} {:<15}".format("Dataset", "Model", "MSE", "R²"))
for dataset_name, model_name, mse, r2 in all_results:
    print(f"{dataset_name:<10} {model_name:<30} {mse:<15.5f} {r2:<15.5f}")
