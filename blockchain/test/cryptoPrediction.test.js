const CryptoPrediction = artifacts.require("CryptoPrediction");

contract("CryptoPrediction", accounts => {
    it("should store a prediction", async () => {
        const instance = await CryptoPrediction.deployed();
        await instance.storePrediction("BTC", 1672531199, 99868.32, { from: accounts[0] });
        
        const predictionCount = await instance.getPredictionCount();
        assert.equal(predictionCount.toNumber(), 1, "Prediction count should be 1");

        const prediction = await instance.getPrediction(0);
        assert.equal(prediction[0], "BTC", "Crypto symbol should be BTC");
        assert.equal(prediction[1].toNumber(), 1672531199, "Prediction date should be 1672531199");
        assert.equal(prediction[2].toNumber(), 99868.32, "Predicted value should be 99868.32");
    });
});
