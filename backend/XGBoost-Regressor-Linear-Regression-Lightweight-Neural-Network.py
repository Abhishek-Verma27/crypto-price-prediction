import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from xgboost import XGBRegressor
import tensorflow as tf
from keras import layers, models
import joblib

# Load data
data = pd.read_csv("data/preprocessed_data.csv")

# Features and target
X = data[['historical_trends', 'sentiment_score', 'macroeconomic_indicator', 'market_cap', 'volume_24h']]
y = data['current_price']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Save scaler
joblib.dump(scaler, "scaler.pkl")

lin_reg = LinearRegression()
lin_reg.fit(X_train_scaled, y_train)
y_pred_lin = lin_reg.predict(X_test_scaled)

print("🔹 Linear Regression")
print("R²:", r2_score(y_test, y_pred_lin))
print("MSE:", mean_squared_error(y_test, y_pred_lin))
joblib.dump(lin_reg, "linear_regressor.pkl")

xgb = XGBRegressor(objective='reg:squarederror', random_state=42, n_estimators=100)
xgb.fit(X_train_scaled, y_train)
y_pred_xgb = xgb.predict(X_test_scaled)

print("🔹 XGBoost Regressor")
print("R²:", r2_score(y_test, y_pred_xgb))
print("MSE:", mean_squared_error(y_test, y_pred_xgb))
joblib.dump(xgb, "xgboost_regressor.pkl")

nn = models.Sequential([
    layers.Input(shape=(X_train_scaled.shape[1],)),
    layers.Dense(16, activation='relu'),
    layers.Dense(8, activation='relu'),
    layers.Dense(1)
])

nn.compile(optimizer='adam', loss='mse')

# Train the model
nn.fit(X_train_scaled, y_train, epochs=50, batch_size=16, verbose=0)

# Evaluate
y_pred_nn = nn.predict(X_test_scaled).flatten()
print("🔹 Neural Network")
print("R²:", r2_score(y_test, y_pred_nn))
print("MSE:", mean_squared_error(y_test, y_pred_nn))

# Save model
nn.save("neural_net_regressor.h5")
