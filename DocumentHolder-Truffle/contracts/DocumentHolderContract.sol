pragma solidity >=0.4.22 <0.9.0;
    contract DocumentHolderContract {
    string public documentHolderID;
	string public documentHolderName;
	string public documentName;
	string public documentFile;
	string public approvedByID;
	string public uploadedByID;
	
    
    function perform_transactions(string memory _documentHolderID, string memory _documentHolderName, string memory _documentName, string memory _documentFile, string memory _approvedByID, string memory _uploadedByID) public{
       documentHolderID = _documentHolderID;
		documentHolderName = _documentHolderName;
		documentName = _documentName;
		documentFile = _documentFile;
		approvedByID = _approvedByID;
		uploadedByID = _uploadedByID;
		
    }
        
}
