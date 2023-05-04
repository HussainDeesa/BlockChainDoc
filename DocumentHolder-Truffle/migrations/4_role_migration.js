const Role = artifacts.require("RoleContract.sol");
        module.exports = function (deployer) {
          deployer.deploy(Role);
        };
        