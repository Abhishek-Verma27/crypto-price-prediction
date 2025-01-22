// scripts/deploy.js
const hre = require("hardhat");

async function main() {
    const PredictionStorage = await hre.ethers.getContractFactory("PredictionStorage");
    console.log("Deploying PredictionStorage contract...");
    
    const predictionStorage = await PredictionStorage.deploy();
    await predictionStorage.deployTransaction.wait();  // Wait for deployment
   
    console.log("PredictionStorage deployed to:", predictionStorage.address);
}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error("Error during deployment:", error);
        process.exit(1);
    });
