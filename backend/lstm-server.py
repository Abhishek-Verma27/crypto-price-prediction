import os
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from web3 import Web3
from keras.models import load_model
from keras.losses import mean_squared_error
import joblib

app = Flask(__name__)
CORS(app)

# === Blockchain Setup ===
skale_url = "https://testnet.skalenodes.com/v1/giant-half-dual-testnet"
web3 = Web3(Web3.HTTPProvider(skale_url))

contract_address = web3.to_checksum_address("0x87DdCCa2876C429bDaeF93497CeBD2898Ca9Da20")
private_key = os.getenv('PRIVATE_KEY')
account = web3.eth.account.from_key(private_key)

contract_abi = [
    {
        "inputs": [
            {"internalType": "string", "name": "cryptoSymbol", "type": "string"},
            {"internalType": "uint256", "name": "predictionDate", "type": "uint256"},
            {"internalType": "uint256", "name": "predictedValue", "type": "uint256"}
        ],
        "name": "storePrediction",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "index", "type": "uint256"}
        ],
        "name": "getPrediction",
        "outputs": [
            {"internalType": "string", "name": "", "type": "string"},
            {"internalType": "uint256", "name": "", "type": "uint256"},
            {"internalType": "uint256", "name": "", "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getPredictionCount",
        "outputs": [
            {"internalType": "uint256", "name": "", "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# === Load LSTM Models and Scalers ===
btc_model = load_model("models/BTC_lstm_model.h5", custom_objects={'mse': mean_squared_error})
eth_model = load_model("models/ETH_lstm_model.h5", custom_objects={'mse': mean_squared_error})

btc_scaler = joblib.load("models/BTC_lstm_scaler.pkl")
eth_scaler = joblib.load("models/ETH_lstm_scaler.pkl")

@app.route("/predict/btc", methods=["POST"])
def predict_btc():
    return make_lstm_prediction(btc_model, btc_scaler, "BTC")

@app.route("/predict/eth", methods=["POST"])
def predict_eth():
    return make_lstm_prediction(eth_model, eth_scaler, "ETH")

def make_lstm_prediction(model, scaler, crypto_type):
    try:
        input_data = request.get_json()
        if not input_data or "sequence" not in input_data:
            return jsonify({"error": "Missing 'sequence' key with 60 raw price values."}), 400
        
        sequence = input_data["sequence"]
        if not isinstance(sequence, list) or len(sequence) != 60:
            return jsonify({"error": "Sequence must be a list of 60 float values."}), 400

        # Convert raw prices to np array and scale
        input_array = np.array(sequence).reshape(-1, 1)
        scaled_input = scaler.transform(input_array).reshape((1, 60, 1))

        # Predict scaled price
        predicted_scaled_price = model.predict(scaled_input)[0][0]

        # Inverse scale to get actual price
        predicted_price = scaler.inverse_transform([[predicted_scaled_price]])[0][0]
        predicted_price_float = float(predicted_price)

        # Blockchain transaction
        gas_price = web3.eth.gas_price
        nonce = web3.eth.get_transaction_count(account.address)

        function_abi = contract.functions.storePrediction(
            crypto_type,
            int(pd.Timestamp.now().timestamp()),
            int(predicted_price_float)
        )._encode_transaction_data()

        tx = {
            'chainId': 974399131,
            'gas': 2000000,
            'gasPrice': gas_price,
            'nonce': nonce,
            'from': account.address,
            'to': contract_address,
            'data': function_abi
        }

        signed_tx = web3.eth.account.sign_transaction(tx, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)

        return jsonify({
            "crypto_type": crypto_type,
            "prediction": predicted_price_float,
            "tx_hash": tx_hash.hex()
        })

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
