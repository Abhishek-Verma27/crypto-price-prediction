from flask import Flask, request, jsonify
import pandas as pd
import joblib

app = Flask(__name__)

# Load the trained model
model_path = "crypto_price_predictor.pkl"
with open(model_path, "rb") as f:
    model = joblib.load(model_path)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Parse JSON input
        input_data = request.get_json()
        df = pd.DataFrame(input_data)

        # Validate input features
        required_features = ["market_cap", "volume_24h", "historical_trends", "sentiment_score", "macroeconomic_indicator"]
        if not all(feature in df.columns for feature in required_features):
            return jsonify({"error": f"Missing required features: {required_features}"}), 400

        # Ensure all required features are numeric
        for feature in required_features:
            if not pd.api.types.is_numeric_dtype(df[feature]):
                return jsonify({"error": f"Feature '{feature}' must be numeric"}), 400

        # Make predictions
        predictions = model.predict(df[required_features])
        return jsonify({"predictions": predictions.tolist()})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
