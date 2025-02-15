"use client";
import React from "react";
import { useState, useCallback } from "react";
import PredictionForm from "../components/Prediction-Form";
import PredictionResult from "../components/Prediction-Result";
import WalletConnect from "../components/Wallet-Connect";

function MainComponent() {
  const [isConnected, setIsConnected] = useState(false);
  const [address, setAddress] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [prediction, setPrediction] = useState(null);
  const handleConnect = useCallback(async () => {
    setLoading(true);
    try {
      if (typeof window.ethereum !== "undefined") {
        const accounts = await window.ethereum.request({
          method: "eth_requestAccounts",
        });
        setAddress(accounts[0]);
        setIsConnected(true);
      } else {
        throw new Error("Please install MetaMask");
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);
  const handleDisconnect = useCallback(() => {
    setAddress("");
    setIsConnected(false);
  }, []);

  const handlePrediction = useCallback(async (values) => {
    setLoading(true);
    setError("");
    try {
        const apiUrl = values.cryptocurrency === "BTC"
            ? "http://127.0.0.1:5000/predict/btc"
            : "http://127.0.0.1:5000/predict/eth";

        const response = await fetch(apiUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify([{
                lag_1: parseFloat(values.lag_1),
                lag_2: parseFloat(values.lag_2),
                lag_3: parseFloat(values.lag_3),
                lag_4: parseFloat(values.lag_4),
                lag_5: parseFloat(values.lag_5)
            }])
        });

        if (!response.ok) {
            throw new Error("Failed to fetch prediction");
        }

        const data = await response.json();
        setPrediction({
            cryptocurrency: values.cryptocurrency,
            predictedPrice: data.prediction,
            transactionHash: data.tx_hash,
            status: "success",
            timestamp: new Date().toISOString(),
        });
    } catch (err) {
        setError(err.message);
    } finally {
        setLoading(false);
    }
}, []);

  return (
    <div className="min-h-screen bg-[#f8f9fa]">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-[#1a1a1a]">
              Crypto Price Predictor
            </h1>
            <WalletConnect
              address={address}
              isConnected={isConnected}
              onConnect={handleConnect}
              onDisconnect={handleDisconnect}
              isLoading={loading}
            />
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid md:grid-cols-2 gap-8">
          <div className="space-y-4">
            <h2 className="text-xl font-semibold text-[#1a1a1a] mb-4">
              Enter Historical Prices
            </h2>
            <PredictionForm
              onSubmit={handlePrediction}
              loading={loading}
              error={error}
            />
          </div>

          <div className="space-y-4">
            <h2 className="text-xl font-semibold text-[#1a1a1a] mb-4">
              Prediction Results
            </h2>
            {prediction ? (
              <PredictionResult
                predictedPrice={prediction.predictedPrice}
                transactionHash={prediction.transactionHash}
                status={prediction.status}
                timestamp={prediction.timestamp}
                cryptocurrency={prediction.cryptocurrency}
              />
            ) : (
              <div className="bg-white rounded-lg shadow-md p-6 max-w-md w-full text-center text-gray-500">
                Submit historical prices to see prediction results
              </div>
            )}
          </div>
        </div>
      </main>

      <style jsx global>{`
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }
        
        .grid > div {
          animation: fadeIn 0.5s ease-out;
        }
      `}</style>
    </div>
  );
}

export default MainComponent;