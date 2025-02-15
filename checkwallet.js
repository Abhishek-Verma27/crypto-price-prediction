const { ethers } = require("hardhat");

async function main() {
  const privateKey = "0x065f0eb0a4b2408bbeac1c66173dac7f92973d3b7508d28f273be32041367a23"; // Replace with your private key
  const wallet = new ethers.Wallet(privateKey);
  console.log("Wallet address:", wallet.address);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
