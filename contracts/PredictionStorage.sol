// contracts/PredictionStorage.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PredictionStorage {
    struct Prediction {
        uint timestamp;
        string cryptocurrency;
        int predictedPrice;
    }

    Prediction[] public predictions;

    function storePrediction(string calldata _cryptocurrency, int _predictedPrice) public {
        predictions.push(Prediction(block.timestamp, _cryptocurrency, _predictedPrice));
    }

    function getPrediction(uint _index) public view returns (uint, string memory, int) {
        Prediction memory prediction = predictions[_index];
        return (prediction.timestamp, prediction.cryptocurrency, prediction.predictedPrice);
    }
}
