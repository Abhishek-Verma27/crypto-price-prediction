from flask import Flask, request, jsonify
import pandas as pd
import joblib
from web3 import Web3

app = Flask(__name__)

# Set the SKALE RPC URL
skale_url = "https://testnet.skalenodes.com/v1/giant-half-dual-testnet"
web3 = Web3(Web3.HTTPProvider(skale_url))

contract_address = web3.to_checksum_address("0x304697ff06FDEF7F2DABb500ee23A5281C3D2c18")
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
account = web3.eth.account.from_key("0x9e371668dcc4151e366a3c25f03d02dbfa62cd4dae5d48ff14cb69147ad713a0")

btc_model_path = r"C:\Users\abhis\OneDrive\Desktop\crypto-price-prediction\backend\models\BTC_price_predictor.pkl"
eth_model_path = r"C:\Users\abhis\OneDrive\Desktop\crypto-price-prediction\backend\models\ETH_price_predictor.pkl"

with open(btc_model_path, "rb") as f:
    btc_model = joblib.load(f)

with open(eth_model_path, "rb") as f:
    eth_model = joblib.load(f)

@app.route("/predict/btc", methods=["POST"])
def predict_btc():
    return make_prediction(btc_model, "BTC")

@app.route("/predict/eth", methods=["POST"])
def predict_eth():
    return make_prediction(eth_model, "ETH")

def make_prediction(model, crypto_type):
    try:
        print("Receiving JSON input...")
        input_data = request.get_json()
        print("Input data received:", input_data)
        
        df = pd.DataFrame(input_data)
        print("DataFrame created:", df)

        required_features = ["lag_1", "lag_2", "lag_3", "lag_4", "lag_5"]
        if not all(feature in df.columns for feature in required_features):
            return jsonify({"error": f"Missing required features: {required_features}"}), 400

        for feature in required_features:
            if not pd.api.types.is_numeric_dtype(df[feature]):
                return jsonify({"error": f"Feature '{feature}' must be numeric"}), 400

        X = df[required_features].to_numpy()
        print("Features array:", X)
        predictions = model.predict(X)
        prediction = int(predictions[0])
        print("Prediction:", prediction)

        function_abi = contract.functions.storePrediction(
            crypto_type, 
            int(pd.Timestamp.now().timestamp()), 
            prediction
        )._encode_transaction_data()
        print("Function ABI created")

        nonce = web3.eth.get_transaction_count(account.address)
        transaction = {
            'chainId': 1,
            'gas': 2000000,
            'gasPrice': web3.eth.gas_price,
            'nonce': nonce,
            'from': account.address,
            'to': contract_address,
            'data': function_abi
        }
        print("Transaction object created:", transaction)

        signed_tx = web3.eth.account.sign_transaction(transaction, account.key)
        print("Transaction signed")

        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)  # Corrected attribute name
        print("Transaction sent, hash:", tx_hash.hex())

        return jsonify({"crypto_type": crypto_type, "prediction": prediction, "tx_hash": tx_hash.hex()})

    except Exception as e:
        print("Error occurred:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
