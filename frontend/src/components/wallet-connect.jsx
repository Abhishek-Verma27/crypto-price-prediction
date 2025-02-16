"use client";
import React from "react";

function WalletConnect({
  address,
  isConnecting,
  isConnected,
  onConnect,
  error,
}) {
  const shortenAddress = (addr) => {
    if (!addr) return "";
    return `${addr.slice(0, 6)}...${addr.slice(-4)}`;
  };

  const [isHovered, setIsHovered] = useState(false);

  return (
    <div className="inline-block">
      {!isConnected && (
        <button
          onClick={onConnect}
          disabled={isConnecting}
          className={`px-4 py-2 rounded-lg font-inter text-sm transition-all ${
            isHovered ? "bg-[#2563eb] text-white" : "bg-[#3b82f6] text-white"
          }`}
          onMouseEnter={() => setIsHovered(true)}
          onMouseLeave={() => setIsHovered(false)}
        >
          {isConnecting ? (
            <span className="flex items-center">
              <i className="fas fa-spinner fa-spin mr-2"></i>
              Connecting...
            </span>
          ) : (
            <span className="flex items-center">
              <i className="fas fa-wallet mr-2"></i>
              Connect Wallet
            </span>
          )}
        </button>
      )}

      {isConnected && (
        <div className="flex items-center px-4 py-2 rounded-lg bg-[#f8fafc] border border-[#e2e8f0]">
          <div className="flex items-center">
            <i className="fas fa-circle text-[#22c55e] text-xs mr-2"></i>
            <span className="font-inter text-sm text-[#64748b]">
              {shortenAddress(address)}
            </span>
          </div>
        </div>
      )}

      {error && (
        <div className="text-[#ef4444] text-sm mt-2 font-inter">{error}</div>
      )}
    </div>
  );
}

function WalletConnectStory() {
  const [isConnected, setIsConnected] = useState(false);
  const [isConnecting, setIsConnecting] = useState(false);
  const [error, setError] = useState(null);
  const [address, setAddress] = useState(null);

  const connectWallet = async () => {
    if (!window.ethereum) {
      setError("Please install MetaMask");
      return;
    }

    setIsConnecting(true);
    setError(null);

    try {
      const accounts = await window.ethereum.request({
        method: "eth_requestAccounts",
      });
      setAddress(accounts[0]);
      setIsConnected(true);
    } catch (err) {
      setError("Failed to connect wallet");
    } finally {
      setIsConnecting(false);
    }
  };

  return (
    <div className="p-8 space-y-4">
      <div>
        <h3 className="font-inter text-lg mb-4">Disconnected State</h3>
        <WalletConnect
          isConnected={false}
          isConnecting={false}
          onConnect={() => {}}
        />
      </div>

      <div>
        <h3 className="font-inter text-lg mb-4">Connecting State</h3>
        <WalletConnect
          isConnected={false}
          isConnecting={true}
          onConnect={() => {}}
        />
      </div>

      <div>
        <h3 className="font-inter text-lg mb-4">Connected State</h3>
        <WalletConnect
          isConnected={true}
          address="0x1234567890abcdef1234567890abcdef12345678"
          onConnect={() => {}}
        />
      </div>

      <div>
        <h3 className="font-inter text-lg mb-4">Error State</h3>
        <WalletConnect
          isConnected={false}
          error="Failed to connect wallet"
          onConnect={() => {}}
        />
      </div>

      <div>
        <h3 className="font-inter text-lg mb-4">Live Demo</h3>
        <WalletConnect
          isConnected={isConnected}
          isConnecting={isConnecting}
          address={address}
          error={error}
          onConnect={connectWallet}
        />
      </div>
    </div>
  );
}

export default WalletConnect;