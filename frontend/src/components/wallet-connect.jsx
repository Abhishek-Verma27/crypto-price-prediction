"use client";
import React from "react";

function WalletConnect({
  address,
  isConnected,
  onConnect,
  onDisconnect,
  isLoading,
}) {
  const shortenAddress = (addr) => {
    if (!addr) return "";
    return `${addr.slice(0, 6)}...${addr.slice(-4)}`;
  };

  return (
    <div className="relative inline-block">
      <button
        onClick={isConnected ? undefined : onConnect}
        className="flex items-center gap-2 px-4 py-2 bg-white border border-gray-200 rounded-full shadow-sm hover:bg-gray-50 transition-colors"
      >
        <div
          className={`w-2 h-2 rounded-full ${
            isLoading
              ? "bg-yellow-400"
              : isConnected
              ? "bg-green-400"
              : "bg-gray-400"
          }`}
        />

        <span className="text-sm font-medium text-gray-700">
          {isLoading
            ? "Connecting..."
            : isConnected
            ? shortenAddress(address)
            : "Connect Wallet"}
        </span>
      </button>

      {isConnected && (
        <button
          onClick={onDisconnect}
          className="absolute mt-2 left-0 w-full px-4 py-2 text-sm text-red-600 bg-white border border-gray-200 rounded-full shadow-sm hover:bg-gray-50 transition-colors"
        >
          Disconnect
        </button>
      )}
    </div>
  );
}

function WalletConnectStory() {
  return (
    <div className="min-h-screen bg-gray-100 p-8 space-y-8">
      <div>
        <h2 className="text-sm font-medium text-gray-500 mb-4">
          Not Connected
        </h2>
        <WalletConnect
          isConnected={false}
          onConnect={() => console.log("Connecting...")}
        />
      </div>

      <div>
        <h2 className="text-sm font-medium text-gray-500 mb-4">Loading</h2>
        <WalletConnect
          isConnected={false}
          isLoading={true}
          onConnect={() => console.log("Connecting...")}
        />
      </div>

      <div>
        <h2 className="text-sm font-medium text-gray-500 mb-4">Connected</h2>
        <WalletConnect
          isConnected={true}
          address="0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
          onDisconnect={() => console.log("Disconnecting...")}
        />
      </div>
    </div>
  );
}

export default WalletConnect;