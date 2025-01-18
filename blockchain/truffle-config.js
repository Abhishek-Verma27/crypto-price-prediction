module.exports = {
  networks: {
    // Local Ganache network configuration
    development: {
      host: "0.0.0.0",     // Localhost
      port: 8545,            // Standard Ethereum port for Ganache
      network_id: "5777",       // Match any network id
    },
    // You can add other network configurations here (e.g., Ropsten, Mainnet)
  },

  // Set default mocha options here, use special reporters, etc.
  mocha: {
    // timeout: 100000
  },

  // Configure your compilers
  compilers: {
    solc: {
      version: "0.8.21",      // Fetch exact version from solc-bin (default: truffle's version)
      // docker: true,        // Use "0.5.1" you've installed locally with docker (default: false)
      // settings: {          // See the solidity docs for advice about optimization and evmVersion
      //  optimizer: {
      //    enabled: false,
      //    runs: 200
      //  },
      //  evmVersion: "byzantium"
      // }
    }
  },
  
  // Truffle DB is currently disabled by default; to enable it, change enabled: false to enabled: true.
  db: {
    enabled: false,
  }
};
