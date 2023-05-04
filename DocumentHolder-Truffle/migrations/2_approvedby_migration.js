const ApprovedBy = artifacts.require("ApprovedByContract.sol");
        module.exports = function (deployer) {
          deployer.deploy(ApprovedBy);
        };
        