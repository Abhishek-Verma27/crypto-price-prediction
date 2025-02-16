"use client";
import React from "react";

function PredictionForm({ onSubmit, loading, error }) {
  const [selectedCoin, setSelectedCoin] = useState("btc");
  const [prices, setPrices] = useState(["", "", "", "", ""]);
  const [validationErrors, setValidationErrors] = useState([]);

  const validatePrices = () => {
    const errors = prices.map((price) => {
      if (!price) return "Price is required";
      if (isNaN(price)) return "Must be a number";
      if (price <= 0) return "Must be greater than 0";
      return "";
    });
    setValidationErrors(errors);
    return errors.every((error) => !error);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validatePrices()) {
      onSubmit({
        coin: selectedCoin,
        prices: prices.map(Number),
      });
    }
  };

  const handleAutoFill = () => {
    const mockData = {
      btc: [44000, 45000, 43000, 46000, 45500],
      eth: [2800, 2850, 2750, 2900, 2850],
    };
    setPrices(mockData[selectedCoin].map(String));
    setValidationErrors([]);
  };

  const updatePrice = (index, value) => {
    const newPrices = [...prices];
    newPrices[index] = value;
    setPrices(newPrices);
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <div className="flex space-x-4 mb-6">
        <button
          onClick={() => setSelectedCoin("btc")}
          className={`px-4 py-2 rounded-lg font-inter ${
            selectedCoin === "btc"
              ? "bg-[#f7931a] text-white"
              : "bg-[#f8fafc] text-[#64748b]"
          }`}
        >
          <i className="fab fa-bitcoin mr-2"></i>
          Bitcoin
        </button>
        <button
          onClick={() => setSelectedCoin("eth")}
          className={`px-4 py-2 rounded-lg font-inter ${
            selectedCoin === "eth"
              ? "bg-[#627eea] text-white"
              : "bg-[#f8fafc] text-[#64748b]"
          }`}
        >
          <i className="fab fa-ethereum mr-2"></i>
          Ethereum
        </button>
      </div>

      <form onSubmit={handleSubmit} className="relative">
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6">
          {prices.map((price, index) => (
            <div key={index}>
              <label className="block font-inter text-sm text-[#64748b] mb-1">
                Day {5 - index}
              </label>
              <input
                type="text"
                value={price}
                onChange={(e) => updatePrice(index, e.target.value)}
                className={`w-full px-3 py-2 rounded-lg border ${
                  validationErrors[index]
                    ? "border-[#ef4444]"
                    : "border-[#e2e8f0]"
                } font-inter text-sm`}
                placeholder="Enter price"
                name={`price-${index}`}
              />
              {validationErrors[index] && (
                <p className="text-[#ef4444] text-xs mt-1 font-inter">
                  {validationErrors[index]}
                </p>
              )}
            </div>
          ))}
        </div>

        <div className="flex justify-between items-center">
          <button
            type="button"
            onClick={handleAutoFill}
            className="px-4 py-2 bg-[#f8fafc] text-[#64748b] rounded-lg font-inter text-sm"
          >
            <i className="fas fa-magic mr-2"></i>
            Auto-fill
          </button>
          <button
            type="submit"
            disabled={loading}
            className="px-6 py-2 bg-[#3b82f6] text-white rounded-lg font-inter text-sm"
          >
            {loading ? (
              <span className="flex items-center">
                <i className="fas fa-circle-notch fa-spin mr-2"></i>
                Predicting...
              </span>
            ) : (
              <span className="flex items-center">
                <i className="fas fa-chart-line mr-2"></i>
                Predict
              </span>
            )}
          </button>
        </div>

        {error && (
          <div className="mt-4 p-4 bg-[#fee2e2] text-[#dc2626] rounded-lg font-inter text-sm">
            {error}
          </div>
        )}
      </form>
    </div>
  );
}

function PredictionFormStory() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (data) => {
    setLoading(true);
    setError(null);
    await new Promise((resolve) => setTimeout(resolve, 2000));
    setLoading(false);
  };

  return (
    <div className="p-8 space-y-8 bg-[#f8fafc]">
      <div>
        <h3 className="font-inter text-lg mb-4">Default State</h3>
        <PredictionForm onSubmit={() => {}} />
      </div>

      <div>
        <h3 className="font-inter text-lg mb-4">Loading State</h3>
        <PredictionForm onSubmit={() => {}} loading={true} />
      </div>

      <div>
        <h3 className="font-inter text-lg mb-4">Error State</h3>
        <PredictionForm onSubmit={() => {}} error="Failed to make prediction" />
      </div>

      <div>
        <h3 className="font-inter text-lg mb-4">Interactive Demo</h3>
        <PredictionForm
          onSubmit={handleSubmit}
          loading={loading}
          error={error}
        />
      </div>
    </div>
  );
}

export default PredictionForm;