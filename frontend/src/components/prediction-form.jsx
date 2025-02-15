import React, { useState } from "react";

function PredictionForm({ onSubmit, loading, error }) {
    const [formData, setFormData] = useState({
        cryptocurrency: "BTC",
        lag_1: "",
        lag_2: "",
        lag_3: "",
        lag_4: "",
        lag_5: ""
    });

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit(formData);
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-4">
            <label className="block">
                Cryptocurrency:
                <select
                    name="cryptocurrency"
                    value={formData.cryptocurrency}
                    onChange={handleChange}
                    className="block w-full mt-1 p-2 border rounded"
                >
                    <option value="BTC">Bitcoin (BTC)</option>
                    <option value="ETH">Ethereum (ETH)</option>
                </select>
            </label>
            
            {[1, 2, 3, 4, 5].map((num) => (
                <label key={num} className="block">
                    Lag {num} Price:
                    <input
                        type="number"
                        name={`lag_${num}`}
                        value={formData[`lag_${num}`]}
                        onChange={handleChange}
                        className="block w-full mt-1 p-2 border rounded"
                        required
                    />
                </label>
            ))}

            {error && <p className="text-red-500">{error}</p>}

            <button 
                type="submit" 
                className="bg-blue-600 text-white p-2 rounded w-full"
                disabled={loading}
            >
                {loading ? "Predicting..." : "Get Prediction"}
            </button>
        </form>
    );
}

export default PredictionForm;
