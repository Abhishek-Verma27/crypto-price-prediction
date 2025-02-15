"use client";
import React from "react";

function PredictionResult({
  predictedPrice,
  transactionHash,
  status,
  timestamp,
}) {
  const formattedPrice = new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(predictedPrice || 0);

  const formattedTime = new Date(timestamp).toLocaleString();

  return (
    <div className="bg-white rounded-lg shadow-md p-6 max-w-md w-full">
      <div className="space-y-6">
        <div className="text-center">
          <h2 className="text-sm font-medium text-gray-500">Predicted Price</h2>
          <div className="mt-2 text-4xl font-bold text-gray-900">
            {formattedPrice}
          </div>
        </div>

        <div className="border-t border-gray-200 pt-4">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-gray-500">Status</span>
            <div
              className={`px-3 py-1 rounded-full text-sm font-medium ${
                status === "success"
                  ? "bg-green-100 text-green-800"
                  : "bg-red-100 text-red-800"
              }`}
            >
              {status === "success" ? "Success" : "Failed"}
            </div>
          </div>
        </div>

        <div className="border-t border-gray-200 pt-4">
          <h3 className="text-sm font-medium text-gray-500">
            Transaction Hash
          </h3>
          <div className="mt-1 break-all text-sm text-gray-900 font-mono">
            {transactionHash || "No transaction hash available"}
          </div>
        </div>

        <div className="border-t border-gray-200 pt-4">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-gray-500">Timestamp</span>
            <span className="text-sm text-gray-900">{formattedTime}</span>
          </div>
        </div>
      </div>
    </div>
  );
}

function PredictionResultStory() {
  return (
    <div className="min-h-screen bg-gray-100 p-6 flex flex-col items-center space-y-6">
      <div className="w-full max-w-md">
        <PredictionResult
          predictedPrice={45123.45}
          transactionHash="0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
          status="success"
          timestamp={new Date().toISOString()}
        />
      </div>

      <div className="w-full max-w-md">
        <PredictionResult
          predictedPrice={0}
          status="failed"
          timestamp={new Date().toISOString()}
        />
      </div>

      <div className="w-full max-w-md">
        <PredictionResult
          predictedPrice={28750.33}
          transactionHash="0x932d35Cc6634C0532925a3b844Bc454e4438f666"
          status="success"
          timestamp={new Date().toISOString()}
        />
      </div>
    </div>
  );
}

export default PredictionResult;