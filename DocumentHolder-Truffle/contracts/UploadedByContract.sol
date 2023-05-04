pragma solidity >=0.4.22 <0.9.0;
    contract UploadedByContract {
    string public uploadedByID;
	
    
    function perform_transactions(string memory _uploadedByID) public{
       uploadedByID = _uploadedByID;
		
    }
        
}
