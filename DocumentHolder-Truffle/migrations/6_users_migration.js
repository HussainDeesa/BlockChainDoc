const Users = artifacts.require("UsersContract.sol");
        module.exports = function (deployer) {
          deployer.deploy(Users);
        };
        