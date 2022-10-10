pragma solidity 0.8.9;

 
contract SimpleSplitwiseV1 {

    mapping (address => mapping(address => uint32)) debts;
    mapping (address => bool) inNetwork;
    address[] network;
    
    function getDebts(address creditor) public view returns (uint32) {
        return debts[msg.sender][creditor];
    }

    function lookup(address debtor, address creditor) public view returns (uint32 ret){
        return debts[debtor][creditor];
    }

    function add_IOU(address creditor, uint32 val) public {
        require (creditor != msg.sender, "Attempted to create IOU to self!");
        debts[msg.sender][creditor]  += val;
        if(!inNetwork[msg.sender]) {
            network.push(msg.sender);
            inNetwork[msg.sender] = 1;
        }
        if(!inNetwork[creditor]) {
            network.push(creditor);
            inNetwork[creditor] = 1;
        }
    }

    function totalOwned(address creditor) public view returns (uint32) {
        uint32 credit = 0;
        uint32 debit = 0;
        uint i;
        for(i=0; i<network.length;i++){
            if(network[i] != creditor){
                credit += debts[network[i]][creditor];
                debit += debts[creditor][network[i]];
            }
        }
        return debit-credit;
    }
}