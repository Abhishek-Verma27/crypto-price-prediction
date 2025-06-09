# Crypto Price Prediction

This project combines machine learning with blockchain to predict cryptocurrency prices based on historical data. Blockchain ensures the transparency and immutability of prediction data while AI models provide price predictions.

![image](https://github.com/user-attachments/assets/219081a6-6909-43ae-b821-2be998a64f39)

![image](https://github.com/user-attachments/assets/676edfeb-e351-4bf6-9b4f-21b2bcfbbc35)

![image](https://github.com/user-attachments/assets/a501a2a4-ed6a-4fed-8be2-f5ba3d7ab555)



## Table of Contents

- [Project Description](#project-description)
- [Features](#features)
- [Technology stack](#technologies-used)
- [Architecture Overview](#architecture-overview)
- [Installation](#installation)
- [Usage](#usage)
- [Frontend](#frontend)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Project Description

Crypto Price Prediction leverages machine learning to forecast prices for popular cryptocurrencies such as Bitcoin (BTC) and Ethereum (ETH). The solution involves:

- **Data Collection:** Historical crypto price data is fetched and preprocessed.
- **AI Model Training:** LSTM and other models are trained to predict future prices.
- **Prediction Storage:** Results are immutably stored on a blockchain via smart contracts, ensuring auditability.
- **User Interface:** A modern web app allows users to interact with the prediction engine and submit their own predictions, which are also stored on-chain.

## Features

- Predicts BTC and ETH prices using LSTM neural networks.
- Stores every prediction on a blockchain for full transparency.
- Responsive frontend built with Streamlit.
- Live price fetching from CoinGecko.
- RESTful API for model inference and blockchain operations.

## Technology Stack

- **Python** (ML backend, Flask API)
- **Solidity** (Smart contracts)
- **Streamlit** (Frontend UI)
- **Hardhat** (Smart contract development)
- **CoinGecko API** (Live and historical price data for model training)

  ## Architecture Overview

```
[User] <-> [Streamlit Frontend] <-> [Flask ML API] <-> [Blockchain (Skale)]
                               |
                        [CoinGecko APIs]
```
- **Frontend:** Streamlit app captures user price inputs and csv uploads, plots the input data on the line graph and displays model prediction outputs and live prices data.
- **Backend:** Flask API serves ML predictions and interacts with the smart contract.
- **Blockchain:** All predictions are stored using Solidity contracts on the Skale network.

## Installation

To get started with the project, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/abhishekverma276/crypto-price-prediction.git
    cd crypto-price-prediction
    ```

2. **Install dependencies**:

    For the backend (Python):
    ```bash
    pip install -r requirements.txt
    ```

    For the frontend (JavaScript):
    ```bash
    npm install
    ```

3. **Compile the Solidity contracts**:
    ```bash
    npx hardhat compile
    ```

## Usage

To use the project, follow these steps:

1. **Start the backend server**:
    ```bash
    python server.py
    ```

2. **Start the frontend server**:
    ```bash
    npm start
    ```

3. **Access the application**:
    Open your web browser and navigate to `http://localhost:3000`.

## Frontend

It is a [Next.js](https://nextjs.org/) project built on React and TailwindCSS.

### Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```
Open http://localhost:3000 with your browser to see the result.

You can start editing the code in src. The page auto-updates as you edit the file.

To learn more, take a look at the following resources:

React Documentation - learn about React
TailwindCSS Documentation - learn about TailwindCSS
Next.js Documentation - learn about Next.js features and API.
Learn Next.js - an interactive Next.js tutorial.
Contributing

We welcome contributions to the project! To contribute, follow these steps:

Fork the repository.
Create a new branch (git checkout -b feature-branch).
Make your changes.
Commit your changes (git commit -m 'Add some feature').
Push to the branch (git push origin feature-branch).
Open a Pull Request.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Contact
For any inquiries, please contact Abhishek Verma.

Code
Feel free to customize the sections further based on the specific details and requirements of your project.
Email: abhishek27.sv@gmail.com

activate virtual environment: venv\Scripts\activate

Request for Bitcoin (/predict/btc):
powershell
$uri = "http://127.0.0.1:5000/predict/btc"
$headers = @{
    "Content-Type" = "application/json"
}
$body = @'
[
  {
    "lag_1": 27408.34,
    "lag_2": 27350.56,
    "lag_3": 27455.23,
    "lag_4": 27500.34,
    "lag_5": 27300.67
  }
]
'@

$response = Invoke-WebRequest -Uri $uri -Headers $headers -Method POST -Body $body
$response.Content
Request for Ethereum (/predict/eth):
powershell
$uri = "http://127.0.0.1:5000/predict/eth"
$headers = @{
    "Content-Type" = "application/json"
}
$body = @'
[
  {
    "lag_1": 1855.97,
    "lag_2": 1849.56,
    "lag_3": 1860.23,
    "lag_4": 1850.34,
    "lag_5": 1830.67
  }
]
'@

$response = Invoke-WebRequest -Uri $uri -Headers $headers -Method POST -Body $body
$response.Content


blockchain commands : 
npx hardhat compile
npx hardhat run scripts/deploy.js --network skale


predict-lstm.py: 
python predict-lstm.py --coin ETH --days 30
python predict-lstm.py --coin BTC --days 30

EXAMPLE API REQUEST FOR LSTM-SERVER: 
POST /predict/btc
Content-Type: application/json

{
  "sequence": [0.234, 0.238, ..., 0.456]  // 60 normalized float values
}
