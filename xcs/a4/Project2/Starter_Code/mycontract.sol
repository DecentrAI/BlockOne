pragma solidity 0.8.9;

 
contract SimpleSplitwiseV3 {

    mapping (address => mapping(address => uint32)) debts;
    
    function getDebts(address creditor) external view returns (uint32) {
        return debts[msg.sender][creditor];
    }

    function lookup(address debtor, address creditor) external view returns (uint32 ret){
        return debts[debtor][creditor];
    }

    function add_IOU(address creditor, uint32 val) external {
        require (creditor != msg.sender, "Attempted to create IOU to self!");
		uint32 reverse = debts[creditor][msg.sender];
		uint32 existing = debts[msg.sender][creditor];
		if(reverse > (existing + val)){
			debts[creditor][msg.sender] -= (existing + val);
			debts[msg.sender][creditor] = 0;
		}		
		else {
			debts[msg.sender][creditor] = existing + val - reverse;
			debts[creditor][msg.sender] = 0;
		}
    }

}