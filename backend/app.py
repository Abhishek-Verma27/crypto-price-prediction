from flask import Flask, request, jsonify
import pickle
import numpy as np
import os
import re

app = Flask(__name__)

# Load the trained model
model_path = "models/price_prediction_model.pkl"
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found at {model_path}. Please ensure the model is trained first.")

with open(model_path, "rb") as model_file:
    model = pickle.load(model_file)

# Helper function to preprocess input data
def preprocess_input(data):
    # Extract the necessary features
    try:
        # Validate and clean each input field
        market_cap = float(data.get("market_cap", 0))
        volume_24h = float(data.get("volume_24h", 0))
        historical_trends = float(data.get("historical_trends", 0))  # Example: past prices or moving averages
        sentiment_score = float(data.get("sentiment_score", 0))  # Example: sentiment score
        macroeconomic_indicator = float(data.get("macroeconomic_indicator", 0))  # Example: inflation rate
        
        # Return as a numpy array for prediction
        return np.array([[market_cap, volume_24h, historical_trends, sentiment_score, macroeconomic_indicator]])
    except ValueError:
        raise ValueError("All input values must be numeric.")

# Define the prediction route
@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get input data from the request
        input_data = request.get_json()

        # Ensure the required fields are present
        if not input_data or len(input_data) == 0:
            return jsonify({"error": "No input data provided"}), 400
        
        # Validate the input fields
        required_fields = ["market_cap", "volume_24h", "historical_trends", "sentiment_score", "macroeconomic_indicator"]
        for field in required_fields:
            if field not in input_data[0]:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        # Process the input data
        processed_data = preprocess_input(input_data[0])

        # Make the prediction
        prediction = model.predict(processed_data)

        # Return the prediction as a JSON response
        return jsonify({"predictions": prediction.tolist()})
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An error occurred while processing the request"}), 500


if __name__ == "__main__":
    app.run(debug=True)
