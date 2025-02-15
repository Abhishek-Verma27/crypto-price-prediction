const { ethers } = require("hardhat");

async function main() {
  const privateKey = "key"; // Replace with your private key
  const wallet = new ethers.Wallet(privateKey);
  console.log("Wallet address:", wallet.address);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
