const UploadedBy = artifacts.require("UploadedByContract.sol");
        module.exports = function (deployer) {
          deployer.deploy(UploadedBy);
        };
        