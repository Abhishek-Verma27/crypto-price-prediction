# Crypto Price Prediction

This project combines machine learning with blockchain to predict cryptocurrency prices based on historical data. Blockchain ensures the transparency and immutability of data used for AI training, while AI models provide price predictions.

## Table of Contents

- [Project Description](#project-description)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Frontend](#frontend)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Project Description

The Crypto Price Prediction project leverages the power of machine learning and blockchain technology to provide accurate predictions of cryptocurrency prices. The project aims to use historical data to train AI models, ensuring data integrity and transparency through blockchain technology.

## Technologies Used

- **JavaScript**: 61.5%
- **Python**: 33.2%
- **Solidity**: 5.1%
- **CSS**: 0.2%

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
