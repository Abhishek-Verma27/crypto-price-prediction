import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import joblib

# Load the combined data
btc_data = pd.read_csv("BITSTAMP_SPOT_BTC_USD_historical_data.csv")
eth_data = pd.read_csv("BITSTAMP_SPOT_ETH_USD_historical_data.csv")

# Function to prepare data for time series forecasting
def prepare_data(crypto_data):
    # Create lag features
    for lag in range(1, 6):
        crypto_data[f'lag_{lag}'] = crypto_data['price_close'].shift(lag)
    # Drop missing values
    crypto_data.dropna(inplace=True)
    return crypto_data

# Preprocess data for Bitcoin and Ethereum
btc_data = prepare_data(btc_data)
eth_data = prepare_data(eth_data)

btc_data.to_csv("preprocessed_btc_data.csv", index=False)
eth_data.to_csv("preprocessed_eth_data.csv", index=False)

# Function to train and evaluate the model for a specific cryptocurrency
def train_and_evaluate(data, crypto_type):
    print(f"Training model for {crypto_type}...")

    # Select features and target variable
    X = data[['lag_1', 'lag_2', 'lag_3', 'lag_4', 'lag_5']]
    y = data['price_close']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Scale the features using StandardScaler
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Define a RandomForestRegressor model
    model = RandomForestRegressor(random_state=42)

    # Set up the hyperparameter grid for tuning
    param_grid = {
        'n_estimators': [50, 100, 150],
        'max_depth': [10, 20, None],
        'min_samples_split': [2, 5],
        'min_samples_leaf': [1, 2],
    }

    # Set up GridSearchCV to search for the best parameters
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=5, n_jobs=-1, scoring='neg_mean_squared_error')

    # Fit the model to the training data
    grid_search.fit(X_train_scaled, y_train)

    # Get the best model from GridSearchCV
    best_model = grid_search.best_estimator_

    # Make predictions on the test set
    y_pred = best_model.predict(X_test_scaled)

    # Calculate the Mean Squared Error and R-squared
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # Output the results
    print(f"Best Model Parameters: {grid_search.best_params_}")
    print(f"Mean Squared Error: {mse}")
    print(f"R-squared: {r2}")
    print(f"Sample Prediction for {crypto_type}: {y_pred[0]}")

    # Save the model
    joblib.dump(best_model, f'{crypto_type}_price_predictor.pkl')

# Load the preprocessed data
btc_data = pd.read_csv("preprocessed_btc_data.csv")
eth_data = pd.read_csv("preprocessed_eth_data.csv")

# Train and evaluate for Bitcoin
train_and_evaluate(btc_data, 'BTC')

# Train and evaluate for Ethereum
train_and_evaluate(eth_data, 'ETH')
