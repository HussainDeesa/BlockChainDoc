const DocumentHolder = artifacts.require("DocumentHolderContract.sol");
        module.exports = function (deployer) {
          deployer.deploy(DocumentHolder);
        };
        