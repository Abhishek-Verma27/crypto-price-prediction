require("@nomiclabs/hardhat-ethers"); // Ensure you have this import

module.exports = {
  solidity: "0.8.28", // Ensure this matches the Solidity version in your contract
  networks: {
    skale: {
      url: "https://testnet.skalenodes.com/v1/giant-half-dual-testnet", // Skale Testnet RPC URL
      chainId: 974399131, // Hardcoded Skale Testnet Chain ID
      accounts: ["065f0eb0a4b2408bbeac1c66173dac7f92973d3b7508d28f273be32041367a23"], // Hardcoded Private Key
    },
  },
};
