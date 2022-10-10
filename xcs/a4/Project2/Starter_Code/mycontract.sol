pragma solidity 0.8.9;

 
contract SimpleSplitwiseV2 {

    mapping (address => mapping(address => uint32)) debts;
    
    function getDebts(address creditor) public view returns (uint32) {
        return debts[msg.sender][creditor];
    }

    function lookup(address debtor, address creditor) public view returns (uint32 ret){
        return debts[debtor][creditor];
    }

    function add_IOU(address creditor, uint32 val) public {
        require (creditor != msg.sender, "Attempted to create IOU to self!");
        debts[msg.sender][creditor]  += val;
    }

}