// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PredictionContract {
    struct Prediction {
        string cryptoSymbol;
        uint256 predictionDate;
        uint256 predictedValue;
    }

    Prediction[] public predictions;

    function storePrediction(string memory cryptoSymbol, uint256 predictionDate, uint256 predictedValue) public {
        predictions.push(Prediction(cryptoSymbol, predictionDate, predictedValue));
    }

    function getPrediction(uint256 index) public view returns (string memory, uint256, uint256) {
        Prediction memory pred = predictions[index];
        return (pred.cryptoSymbol, pred.predictionDate, pred.predictedValue);
    }

    function getPredictionCount() public view returns (uint256) {
        return predictions.length;
    }
}
