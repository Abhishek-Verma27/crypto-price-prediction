const { ethers } = require("hardhat");

async function main() {
const privateKey = process.env.PRIVATE_KEY;  const wallet = new ethers.Wallet(privateKey);
  console.log("Wallet address:", wallet.address);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
