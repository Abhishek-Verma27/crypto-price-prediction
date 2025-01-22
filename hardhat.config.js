require("@nomicfoundation/hardhat-ethers");
require("dotenv").config();
const { SKALE_PRIVATE_KEY, SKALE_ENDPOINT } = process.env;

module.exports = {
    solidity: "0.8.28",
    networks: {
        skale: {
            url: SKALE_ENDPOINT,
            accounts: [`0x${SKALE_PRIVATE_KEY}`],
        },
    },
};
