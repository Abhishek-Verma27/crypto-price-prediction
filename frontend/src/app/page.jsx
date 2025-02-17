"use client";
import {React, useState, useEffect} from "react";
import WalletConnect from "../components/Wallet-Connect";
import PriceDisplay from "../components/Price-Display";
import PredictionForm from "../components/Prediction-Form";
import TransactionStatus from "../components/Transaction-Status";

function MainComponent() {
  const [walletState, setWalletState] = useState({
    isConnected: false,
    isConnecting: false,
    address: null,
    error: null,
  });

  const [prices, setPrices] = useState(null);
  const [priceLoading, setPriceLoading] = useState(true);
  const [priceError, setPriceError] = useState(null);

  const [prediction, setPrediction] = useState(null);
  const [predictionLoading, setPredictionLoading] = useState(false);
  const [transactionStatus, setTransactionStatus] = useState(null);
  const [transactionHash, setTransactionHash] = useState(null);
  const [transactionError, setTransactionError] = useState(null);

  useEffect(() => {
    const fetchPrices = async () => {
      try {
        const response = await fetch("https://api.binance.com/api/v3/ticker/24hr");
        if (!response.ok) throw new Error(`Error ${response.status}: ${response.statusText}`);
  
        const data = await response.json();
  
        // Extract relevant data for BTC and ETH
        const btcData = data.find((item) => item.symbol === "BTCUSDT");
        const ethData = data.find((item) => item.symbol === "ETHUSDT");
  
        setPrices({
          btc: {
            current: parseFloat(btcData.lastPrice),
            changePercentage: parseFloat(btcData.priceChangePercent),
          },
          eth: {
            current: parseFloat(ethData.lastPrice),
            changePercentage: parseFloat(ethData.priceChangePercent),
          },
        });
  
        setPriceLoading(false);
      } catch (error) {
        setPriceError(error.message);
        setPriceLoading(false);
      }
    };
  
    fetchPrices();
    const interval = setInterval(fetchPrices, 60000);
    return () => clearInterval(interval);
  }, []);  

  const handleWalletConnect = async () => {
    if (!window.ethereum) {
      setWalletState((prev) => ({ ...prev, error: "Please install MetaMask" }));
      return;
    }

    setWalletState((prev) => ({ ...prev, isConnecting: true, error: null }));

    try {
      const accounts = await window.ethereum.request({
        method: "eth_requestAccounts",
      });
      setWalletState((prev) => ({
        ...prev,
        address: accounts[0],
        isConnected: true,
        isConnecting: false,
      }));
    } catch (err) {
      setWalletState((prev) => ({
        ...prev,
        error: "Failed to connect wallet",
        isConnecting: false,
      }));
    }
  };

  const handlePredictionSubmit = async (data) => {
    setPredictionLoading(true);
    setTransactionError(null);
    const cryptoType = data.coin; // Extract cryptoType from data
    delete data.coin; // Remove coin key from data before sending

    try {
      const response = await fetch(`http://127.0.0.1:5000/predict/${cryptoType}`, { // Dynamic URL based on cryptoType
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify([data]), // Make sure data is in a list as per backend requirement
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`API error: ${errorText}`);
      }

      const result = await response.json();

      if (result.error) {
        throw new Error(result.error);
      }

      // Set prediction with the coin type included
      setPrediction({ coin: cryptoType, price: result.prediction });
      setTransactionStatus('success');
      setTransactionHash(result.tx_hash);
    } catch (err) {
      setTransactionError(err.message || "Transaction failed");
      setTransactionStatus('failure');
    } finally {
      setPredictionLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#f8fafc]">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center">
              <i className="fas fa-chart-line text-[#3b82f6] text-2xl mr-3"></i>
              <h1 className="font-inter text-2xl font-bold text-[#1e293b]">
                Crypto Price Predictor
              </h1>
            </div>
            <WalletConnect
              isConnected={walletState.isConnected}
              isConnecting={walletState.isConnecting}
              address={walletState.address}
              error={walletState.error}
              onConnect={handleWalletConnect}
            />
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="space-y-8">
          <PriceDisplay
            prices={prices}
            loading={priceLoading}
            error={priceError}
          />

          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="font-inter text-xl font-semibold mb-4">
              Make Your Prediction
            </h2>
            <p className="font-inter text-[#64748b] mb-6">
              Enter the predicted prices for the 5 days to generate a
              forecast. Connect your wallet to save your predictions.
            </p>
            <PredictionForm
              onSubmit={handlePredictionSubmit}
              loading={predictionLoading}
              error={transactionError}
            />
          </div>

          {(prediction || transactionStatus) && (
            <div className="transition-all duration-300 ease-in-out">
              <TransactionStatus
                prediction={prediction}
                transactionStatus={transactionStatus}
                transactionHash={transactionHash}
                error={transactionError}
              />
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default MainComponent;