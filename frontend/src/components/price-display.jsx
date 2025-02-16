"use client";
import React from "react";

function PriceDisplay({ prices, loading, error }) {
  const [chartData, setChartData] = useState({
    btc: Array.from({ length: 5 }).fill(0),
    eth: Array.from({ length: 5 }).fill(0),
  });

  useEffect(() => {
    if (prices?.btc?.history) {
      setChartData({
        btc: prices.btc.history,
        eth: prices.eth.history,
      });
    }
  }, [prices]);

  const formatPrice = (price) => {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    }).format(price);
  };

  const formatPercentage = (percentage) => {
    const value = percentage?.toFixed(2) || 0;
    const isPositive = value >= 0;
    return (
      <span className={`${isPositive ? "text-[#22c55e]" : "text-[#ef4444]"}`}>
        {isPositive ? "↑" : "↓"} {Math.abs(value)}%
      </span>
    );
  };

  if (error) {
    return (
      <div className="p-6 bg-[#fee2e2] rounded-lg">
        <p className="text-[#dc2626] font-inter">Error loading price data</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      {["btc", "eth"].map((coin) => (
        <div
          key={coin}
          className="bg-white rounded-xl shadow-lg p-6 relative overflow-hidden"
        >
          <div
            className={`transition-opacity duration-300 ${
              loading ? "opacity-50" : "opacity-100"
            }`}
          >
            <div className="flex justify-between items-center mb-4">
              <div className="flex items-center">
                <i
                  className={`fab fa-${
                    coin === "btc" ? "bitcoin" : "ethereum"
                  } text-2xl mr-2 ${
                    coin === "btc" ? "text-[#f7931a]" : "text-[#627eea]"
                  }`}
                ></i>
                <h2 className="font-inter text-xl">{coin.toUpperCase()}/USD</h2>
              </div>
              {prices?.[coin]?.changePercentage && (
                <div className="font-inter text-sm">
                  {formatPercentage(prices[coin].changePercentage)}
                </div>
              )}
            </div>

            <div className="mb-4">
              <span className="font-inter text-3xl font-bold">
                {prices?.[coin]?.current
                  ? formatPrice(prices[coin].current)
                  : "--"}
              </span>
            </div>

            {chartData[coin].length > 0 && (
              <div className="h-[60px] w-full">
                <svg viewBox="0 0 100 20" className="w-full h-full">
                  <path
                    d={`M ${chartData[coin]
                      .map(
                        (price, index) =>
                          `${index * 25},${
                            20 - (price / Math.max(...chartData[coin])) * 20
                          }`
                      )
                      .join(" L ")}`}
                    fill="none"
                    stroke={coin === "btc" ? "#f7931a" : "#627eea"}
                    strokeWidth="0.5"
                  />
                </svg>
              </div>
            )}
          </div>

          {loading && (
            <div className="absolute inset-0 bg-white bg-opacity-50 flex items-center justify-center">
              <i className="fas fa-circle-notch fa-spin text-[#3b82f6] text-2xl"></i>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}

function PriceDisplayStory() {
  const mockPrices = {
    btc: {
      current: 45000,
      changePercentage: 2.5,
      history: [42000, 43000, 44000, 45000, 45000],
    },
    eth: {
      current: 2800,
      changePercentage: -1.2,
      history: [2900, 2850, 2800, 2750, 2800],
    },
  };

  return (
    <div className="p-8 space-y-8 bg-[#f8fafc]">
      <div>
        <h3 className="font-inter text-lg mb-4">Loading State</h3>
        <PriceDisplay loading={true} />
      </div>

      <div>
        <h3 className="font-inter text-lg mb-4">Error State</h3>
        <PriceDisplay error="Failed to fetch prices" />
      </div>

      <div>
        <h3 className="font-inter text-lg mb-4">Populated State</h3>
        <PriceDisplay prices={mockPrices} loading={false} />
      </div>
    </div>
  );
}

export default PriceDisplay;