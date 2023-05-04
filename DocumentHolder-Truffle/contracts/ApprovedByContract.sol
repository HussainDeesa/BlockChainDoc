pragma solidity >=0.4.22 <0.9.0;
    contract ApprovedByContract {
    string public approvedByID;
	
    
    function perform_transactions(string memory _approvedByID) public{
       approvedByID = _approvedByID;
		
    }
        
}
