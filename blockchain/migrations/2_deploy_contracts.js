const CryptoPrediction = artifacts.require("CryptoPrediction");

module.exports = function(deployer) {
    deployer.deploy(CryptoPrediction);
};
