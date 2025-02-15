const { ethers } = require("hardhat");

async function main() {
  // Get the wallet address from your environment variable or hardcoded value
  const [deployer] = await ethers.getSigners();
  
  // Print the deployer's address
  console.log("Deploying contracts with the account:", deployer.address);
  
  // Check the balance of the wallet (in SFuel)
  const balance = await deployer.getBalance();
  console.log("Wallet balance:", ethers.utils.formatUnits(balance, 18), "SFuel");
  
  // If the balance is too low, exit the script
  if (balance.lt(ethers.utils.parseUnits("0.5", 18))) {
    console.log("Not enough SFuel in the wallet to deploy the contract.");
    return;
  }

  // Deploy your contract here (for example)
  const Contract = await ethers.getContractFactory("PredictionContract");
  const contract = await Contract.deploy();
  
  console.log("Contract deployed to:", contract.address);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
