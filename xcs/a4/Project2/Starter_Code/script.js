getLastActive// =============================================================================
//                                  Config
// =============================================================================

let web3 = new Web3(Web3.givenProvider || "ws://localhost:8545");

// Constant we use later
var GENESIS = '0x0000000000000000000000000000000000000000000000000000000000000000';

// This is the ABI for your contract (get it from Remix, in the 'Compile' tab)
// ============================================================
var abi = [
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "creditor",
				"type": "address"
			},
			{
				"internalType": "uint32",
				"name": "val",
				"type": "uint32"
			}
		],
		"name": "add_IOU",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "creditor",
				"type": "address"
			}
		],
		"name": "getDebts",
		"outputs": [
			{
				"internalType": "uint32",
				"name": "",
				"type": "uint32"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "debtor",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "creditor",
				"type": "address"
			}
		],
		"name": "lookup",
		"outputs": [
			{
				"internalType": "uint32",
				"name": "ret",
				"type": "uint32"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]; // FIXME: fill this in with your contract's ABI //Be sure to only have one array, not two

// ============================================================
abiDecoder.addABI(abi);
// call abiDecoder.decodeMethod to use this - see 'getAllFunctionCalls' for more

var contractAddress = '0x4be71F0080e24d2e207f3f5254c0F3454D23C6f7'; // FIXME: fill this in with your contract's address/hash
var BlockchainSplitwise = new web3.eth.Contract(abi, contractAddress);

// =============================================================================
//                            Functions To Implement
// =============================================================================

// TODO: Add any helper functions here!

async function unsafeIOU(debtor, creditor, amount){
	return BlockchainSplitwise.methods.add_IOU(creditor, amount).send({from: debtor});	
}

async function creditorList(debtor) {
	var userList = await getUsers();
	var creditorChain = [];
	for(i=0; i<userList.length; i++){
		if(userList[i] != debtor){
			credit = await BlockchainSplitwise.methods.lookup(debtor, userList[i]).call();
			if(credit > 0)
				creditorChain.push({
					user : userList[i],
					val : credit
				});
		}
	}
	return creditorChain;
}


async function creditorChain(start, end) {
	var queue = [[{
					user : start,
					val : 0
				}]];
	while (queue.length > 0) {
		var cur = queue.shift();
		var lastNode = cur[cur.length-1]
		if (lastNode.user === end) {
			return cur;
		} else {
			var neighbors = await creditorList(lastNode.user);
			for (var i = 0; i < neighbors.length; i++) {
				queue.push(cur.concat([neighbors[i]]));
			}
		}
	}
	return null;
}


async function getIdOf(user){
	var accounts = await web3.eth.getAccounts();
	for(var i=0; i<accounts.length; i++){
		if(accounts[i].toLowerCase() == user.toLowerCase())
			return i;
	}
	return null;
}


// TODO: Return a list of all users (creditors or debtors) in the system
// You can return either:
//   - a list of everyone who has ever sent or received an IOU
// OR
//   - a list of everyone currently owing or being owed money
async function getUsers() {
	var defaultAccount = web3.eth.defaultAccount;
	const usersList = new Set();
	func_calls = await getAllFunctionCalls(contractAddress, "add_IOU");
	for(var i=0; i< func_calls.length;i++){
		usersList.add(func_calls[i].from.toLowerCase());
		usersList.add(func_calls[i].args[0].toLowerCase());
	}
	web3.eth.defaultAccount = defaultAccount;
	return Array.from(usersList);
}

// TODO: Get the total amount owed by the user specified by 'user'
async function getTotalOwed(user) {
	var totalOwned = 0;
	// contract based method (v1)
	// not working due to low gas limit
	// totalOwned = BlockchainSplitwise.methods.totalOwned(user).call({from: web3.eth.defaultAccount});
	// end contract based
	user = user.toLowerCase();
	var userList = await getUsers();
	var credit = 0;
	var debit = 0;
	for(i=0; i<userList.length; i++){
		if(userList[i] != user){
			debit += await await BlockchainSplitwise.methods.lookup(user, userList[i]).call();
			credit += await await BlockchainSplitwise.methods.lookup(userList[i], user).call();
		}
	}
	totalOwned = debit - credit;
	return totalOwned;
}

// TODO: Get the last time this user has sent or received an IOU, in seconds since Jan. 1, 1970
// Return null if you can't find any activity for the user.
// HINT: Try looking at the way 'getAllFunctionCalls' is written. You can modify it if you'd like.
async function getLastActive(user) {
	user = user.toLowerCase()
	var lastActive = 0;
	func_calls = await getAllFunctionCalls(contractAddress, "add_IOU");
	for(var i=0; i< func_calls.length;i++){
		if((func_calls[i].from == user || func_calls[i].args[0] == user) && func_calls[i].t > lastActive){
				lastActive = func_calls[i].t;
		}
	}
	return lastActive;
}


// TODO: add an IOU ('I owe you') to the system
// The person you owe money is passed as 'creditor'
// The amount you owe them is passed as 'amount'
async function add_IOU(creditor, amount, userList = null) {
	if(web3.eth.defaultAccount.toLowerCase() == creditor.toLowerCase())
		return Promise.reject(new Error('Cannot own to yourself'));
	//var reverse_chain = await doBFS(creditor.toLowerCase(), web3.eth.defaultAccount.toLowerCase(), creditorList);
	var reverse_chain = await creditorChain(creditor.toLowerCase(), web3.eth.defaultAccount.toLowerCase());
	var id_debtor = web3.eth.defaultAccount.toLowerCase();
	var id_creditor = creditor;
	if(userList != null){
		id_creditor = await getIdOf(creditor, userList);
		id_debtor = await getIdOf(web3.eth.defaultAccount, userList);
	}
	if(reverse_chain == null){
		console.log(`No reverse loop found between ${id_debtor} and ${id_creditor}`);
		return BlockchainSplitwise.methods.add_IOU(creditor, amount).send({from: web3.eth.defaultAccount});
	}
	else {
		console.log(`Reverse loop found between ${id_debtor} and ${id_creditor}`)
		var pairs = [{
			debtor : web3.eth.defaultAccount.toLowerCase(),
			creditor : creditor,
			amount : amount,
		}];
		var min_debt = parseInt(amount);
		var min_pair = 0
		for(var j=1; j<reverse_chain.length;j++){
			pairs.push({
				debtor : reverse_chain[j-1].user,
				creditor : reverse_chain[j].user,
				amount : reverse_chain[j].val
			});
			if(min_debt > parseInt(reverse_chain[j].val)){
				min_debt = parseInt(reverse_chain[j].val);
				min_pair = j;
			}
		}
		
		for(var j=0;j<pairs.length;j++){
			var s_d = '';
			var s_c = '';
			if(userList != null){
				s_d = await getIdOf(pairs[j].debtor, userList);
				s_c = await getIdOf(pairs[j].creditor, userList);
			} else{
				s_d = pairs[j].debtor;
				s_c = pairs[j].creditor;
			}
			console.log(s_d + ' ownes ' + pairs[j].amount + ' to ' + s_c + ' but is decreased by ' + min_debt);
			if(j==0){
				if((amount - min_debt) > 0){
					// current unsent transaction
					var res = await BlockchainSplitwise.methods.add_IOU(creditor, amount - min_debt).send({from: web3.eth.defaultAccount});
				}
			} else {
				var s_amount = ""+min_debt+"";
				var res = await unsafeIOU(pairs[j].creditor, pairs[j].debtor, s_amount);
			}
			
		}		
	}		
}

// =============================================================================
//                              Provided Functions
// =============================================================================
// Reading and understanding these should help you implement the above

// This searches the block history for all calls to 'functionName' (string) on the 'addressOfContract' (string) contract
// It returns an array of objects, one for each call, containing the sender ('from'), arguments ('args'), and the timestamp ('t')
async function getAllFunctionCalls(addressOfContract, functionName) {
	var curBlock = await web3.eth.getBlockNumber();
	var function_calls = [];

	while (curBlock !== GENESIS) {
	  var b = await web3.eth.getBlock(curBlock, true);
	  var txns = b.transactions;
	  for (var j = 0; j < txns.length; j++) {
	  	var txn = txns[j];

	  	// check that destination of txn is our contract
			if(txn.to == null){continue;}
	  	if (txn.to.toLowerCase() === addressOfContract.toLowerCase()) {
	  		var func_call = abiDecoder.decodeMethod(txn.input);

			// check that the function getting called in this txn is 'functionName'
			if (func_call && func_call.name === functionName) {
				var time = await web3.eth.getBlock(curBlock);
	  			var args = func_call.params.map(function (x) {return x.value});
	  			function_calls.push({
	  				from: txn.from.toLowerCase(),
	  				args: args,
					t: time.timestamp
	  			})
	  		}
	  	}
	  }
	  curBlock = b.parentHash;
	}
	return function_calls;
}

// We've provided a breadth-first search implementation for you, if that's useful
// It will find a path from start to end (or return null if none exists)
// You just need to pass in a function ('getNeighbors') that takes a node (string) and returns its neighbors (as an array)
async function doBFS(start, end, getNeighbors) {
	var queue = [[start]];
	while (queue.length > 0) {
		var cur = queue.shift();
		var lastNode = cur[cur.length-1]
		if (lastNode === end) {
			return cur;
		} else {
			var neighbors = await getNeighbors(lastNode);
			for (var i = 0; i < neighbors.length; i++) {
				queue.push(cur.concat([neighbors[i]]));
			}
		}
	}
	return null;
}

// =============================================================================
//                                      UI
// =============================================================================

// This sets the default account on load and displays the total owed to that
// account.
web3.eth.getAccounts().then((response)=> {
	web3.eth.defaultAccount = response[0];

	getTotalOwed(web3.eth.defaultAccount).then((response)=>{
		$("#total_owed").html("$"+response);
	});

	getLastActive(web3.eth.defaultAccount).then((response)=>{
		time = timeConverter(response)
		$("#last_active").html(time)
	});
});

// This code updates the 'My Account' UI with the results of your functions
$("#myaccount").change(function() {
	web3.eth.defaultAccount = $(this).val();

	getTotalOwed(web3.eth.defaultAccount).then((response)=>{
		$("#total_owed").html("$"+response);
	})

	getLastActive(web3.eth.defaultAccount).then((response)=>{
		time = timeConverter(response)
		$("#last_active").html(time)
	});
});

// Allows switching between accounts in 'My Account' and the 'fast-copy' in 'Address of person you owe
web3.eth.getAccounts().then((response)=>{
	var opts = response.map(function (a) { return '<option value="'+
			a.toLowerCase()+'">'+a.toLowerCase()+'</option>' });
	$(".account").html(opts);
	$(".wallet_addresses").html(response.map(function (a) { return '<li>'+a.toLowerCase()+'</li>' }));
});

// This code updates the 'Users' list in the UI with the results of your function
getUsers().then((response)=>{
	$("#all_users").html(response.map(function (u,i) { return "<li>"+u+"</li>" }));
});

// This runs the 'add_IOU' function when you click the button
// It passes the values from the two inputs above
$("#addiou").click(function() {
	web3.eth.defaultAccount = $("#myaccount").val(); //sets the default account
  add_IOU($("#creditor").val(), $("#amount").val()).then((response)=>{
		window.location.reload(true); // refreshes the page after add_IOU returns and the promise is unwrapped
	})
});

// This is a log function, provided if you want to display things to the page instead of the JavaScript console
// Pass in a discription of what you're printing, and then the object to print
function log(description, obj) {
	$("#log").html($("#log").html() + description + ": " + JSON.stringify(obj, null, 2) + "\n\n");
}


// =============================================================================
//                                      TESTING
// =============================================================================

// This section contains a sanity check test that you can use to ensure your code
// works. We will be testing your code this way, so make sure you at least pass
// the given test. You are encouraged to write more tests!

// Remember: the tests will assume that each of the four client functions are
// async functions and thus will return a promise. Make sure you understand what this means.

function check(name, condition) {
	if (condition) {
		console.log(name + ": SUCCESS");
		return 3;
	} else {
		console.log(name + ": FAILED");
		return 0;
	}
}

async function sanityCheck() {
	console.log ("\nTEST", "Simplest possible test: only runs one add_IOU; uses all client functions: lookup, getTotalOwed, getUsers, getLastActive");

	var score = 0;

	var accounts = await web3.eth.getAccounts();
	web3.eth.defaultAccount = accounts[0];
	console.log("Default account", web3.eth.defaultAccount);

	var users = await getUsers();
	score += check("getUsers() initially empty", users.length === 0);

	var owed = await getTotalOwed(accounts[0]);
	score += check("getTotalOwed(0) initially empty", owed === 0);

	var lookup_0_1 = await BlockchainSplitwise.methods.lookup(accounts[0], accounts[1]).call({from:web3.eth.defaultAccount});
	score += check("lookup(0,1) initially 0", parseInt(lookup_0_1, 10) === 0);

	var response = await add_IOU(accounts[1], "10");

	users = await getUsers();
	score += check("getUsers() now length 2", users.length === 2);

	owed = await getTotalOwed(accounts[0]);
	score += check("getTotalOwed(0) now 10", owed === 10);

	lookup_0_1 = await BlockchainSplitwise.methods.lookup(accounts[0], accounts[1]).call({from:web3.eth.defaultAccount});
	score += check("lookup(0,1) now 10", parseInt(lookup_0_1, 10) === 10);

	var timeLastActive = await getLastActive(accounts[0]);
	var timeNow = Date.now()/1000;
	var difference = timeNow - timeLastActive;
	score += check("getLastActive(0) works", difference <= 60 && difference >= -3); // -3 to 60 seconds

	console.log("Final Score: " + score +"/21");

	web3.eth.defaultAccount = accounts[1]
	console.log('Back 1-[3]->0')
	var response = await add_IOU(accounts[0], "3");
	lookup_0_1 = await BlockchainSplitwise.methods.lookup(accounts[0], accounts[1]).call({from:web3.eth.defaultAccount});	
	console.log("after 1-to-0=3", lookup_0_1);
	console.log('Back 1-[7]->0')
	var response = await add_IOU(accounts[0], "7");
	lookup_0_1 = await BlockchainSplitwise.methods.lookup(accounts[0], accounts[1]).call({from:web3.eth.defaultAccount});	
	console.log("after 1-to-0=7", lookup_0_1);
	
	console.log("owning to yourself");
	web3.eth.defaultAccount = accounts[1]
	try{
		var response = await add_IOU(accounts[1], "10");
		console.log("Not good!!! owning to yourself did not generate exception");
	} catch(e){
		console.log("Error", e);
	}
	
	console.log(response);

	// 5 -- [03] --> 3
	// 2 -- [28] --> 9

	// cycle {
		// 2 -- [30] --> 4
		// 4 -- [12] --> 6
		// 6 -- [30] --> 5
		// 5 -- [22] --> 7
		// 7 -- [01] --> 1
		// 1 -- [23] --> 8
		// 8 -- [16] --> 0
		// 0 -- [09] --> 2
	// }
	var pairs = [[5,3,3],[2,28,9],[2,30,4],[4,12,6],[6,30,5],[5,22,7],[7,1,1],[1,23,8],[8,16,0],[0,9,2]]
	for(var i=0;i<pairs.length;i++){
		debtor = pairs[i][0];
		val = pairs[i][1];
		creditor = pairs[i][2];
		console.log(debtor + ' -- ['+val+'] --> '+creditor);
		web3.eth.defaultAccount = accounts[debtor];
		var res = await add_IOU(accounts[creditor], "" + val +"", accounts);
	}
	
	console.log('Revisiting debts');
	for(var i=0;i<pairs.length;i++){
		debtor = pairs[i][0];
		creditor = pairs[i][2];
		lookup_res = await BlockchainSplitwise.methods.lookup(accounts[debtor], accounts[creditor]).call({from:web3.eth.defaultAccount});
		console.log(debtor + ' - ['+lookup_res+'] -> '+creditor);
	}
		
}

sanityCheck() //Uncomment this line to run the sanity check when you first open index.html
