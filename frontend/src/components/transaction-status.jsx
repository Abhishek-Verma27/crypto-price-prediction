"use client";
import {React, useState} from "react";

function TransactionStatus({
  prediction,
  transactionStatus,
  transactionHash,
  error,
}) {
  const [copied, setCopied] = useState(false);

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(transactionHash);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error("Failed to copy:", err);
    }
  };

  const getStatusColor = () => {
    switch (transactionStatus) {
      case "success":
        return "text-[#22c55e]";
      case "failure":
        return "text-[#ef4444]";
      default:
        return "text-[#3b82f6]";
    }
  };

  const getStatusIcon = () => {
    switch (transactionStatus) {
      case "success":
        return "fa-check-circle";
      case "failure":
        return "fa-times-circle";
      default:
        return "fa-circle-notch fa-spin";
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      {prediction && (
        <div className="mb-6">
          <h2 className="font-inter text-xl mb-4">Prediction Results</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-[#f8fafc] p-4 rounded-lg">
              <span className="font-inter text-sm text-[#64748b]">Coin</span>
              <div className="font-inter text-lg">
                {prediction.coin === "btc" ? (
                  <span>
                    <i className="fab fa-bitcoin text-[#f7931a] mr-2"></i>
                    Bitcoin
                  </span>
                ) : (
                  <span>
                    <i className="fab fa-ethereum text-[#627eea] mr-2"></i>
                    Ethereum
                  </span>
                )}
              </div>
            </div>
            <div className="bg-[#f8fafc] p-4 rounded-lg">
              <span className="font-inter text-sm text-[#64748b]">
                Predicted Price
              </span>
              <div className="font-inter text-lg">
                {prediction.price !== undefined ? `$${prediction.price.toLocaleString()}` : 'N/A'}
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="border-t border-[#e2e8f0] pt-6">
        <div className="flex items-center mb-4">
          <i
            className={`fas ${getStatusIcon()} ${getStatusColor()} text-xl mr-2`}
          ></i>
          <span className={`font-inter ${getStatusColor()}`}>
            {transactionStatus === "pending"
              ? "Transaction Pending"
              : transactionStatus === "success"
              ? "Transaction Successful"
              : transactionStatus === "failure"
              ? "Transaction Failed"
              : "Unknown Status"}
          </span>
        </div>

        {transactionHash && (
          <div className="space-y-4">
            <div className="flex items-center justify-between bg-[#f8fafc] p-3 rounded-lg">
              <div className="font-inter text-sm text-[#64748b] truncate mr-2">
                {transactionHash}
              </div>
              <button
                onClick={copyToClipboard}
                className="text-[#3b82f6] hover:text-[#2563eb] transition-colors"
              >
                <i className={`fas ${copied ? "fa-check" : "fa-copy"}`}></i>
              </button>
            </div>

            <a
              href={`https://giant-half-dual-testnet.explorer.testnet.skalenodes.com/address/0x87DdCCa2876C429bDaeF93497CeBD2898Ca9Da20`}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-block text-[#3b82f6] hover:text-[#2563eb] font-inter text-sm"
            >
              <i className="fas fa-external-link-alt mr-2"></i>
              View on Skale Explorer
            </a>
          </div>
        )}

        {error && (
          <div className="mt-4 p-4 bg-[#fee2e2] text-[#dc2626] rounded-lg font-inter text-sm">
            {error}
          </div>
        )}
      </div>
    </div>
  );
}

export default TransactionStatus;
