include "./mimc.circom";

/*
 * IfThenElse sets `out` to `true_value` if `condition` is 1 and `out` to
 * `false_value` if `condition` is 0.
 *
 * It enforces that `condition` is 0 or 1.
 *
 */
template IfThenElse() {
    signal input condition;
    signal input true_value;
    signal input false_value;
    signal output out;

    // TODO	
    // Hint: You will need a helper signal...
	condition * (condition - 1) === 0;
	signal helper_signal;
	helper_signal <== (1 - condition) * false_value;	
	out <== condition * true_value + helper_signal;
}

/*
 * SelectiveSwitch takes two data inputs (`in0`, `in1`) and produces two ouputs.
 * If the "select" (`s`) input is 1, then it inverts the order of the inputs
 * in the ouput. If `s` is 0, then it preserves the order.
 *
 * It enforces that `s` is 0 or 1.
 */
template SelectiveSwitch() {
    signal input in0;
    signal input in1;
    signal input s;
    signal output out0;
    signal output out1;

    // TODO
	s * (s - 1) === 0;
	
	component If0 = IfThenElse();
	component If1 = IfThenElse();
	
	If0.condition <== s;
	If0.true_value <== in1;
	If0.false_value <== in0;

	If1.condition <== s;
	If1.true_value <== in0;
	If1.false_value <== in1;
	
	out0 <== If0.out;
	out1 <== If1.out;
	
    // signal helper;
	// s * (s - 1) === 0;
	// helper <== (in0 - in1) * s;    // We create aux in order to have only one multiplication
    // out0 <== helper + in0;
    // out1 <== -helper + in1;	
}

/*
 * Verifies the presence of H(`nullifier`, `nonce`) in the tree of depth
 * `depth`, summarized by `digest`.
 * This presence is witnessed by a Merle proof provided as
 * the additional inputs `sibling` and `direction`, 
 * which have the following meaning:
 *   sibling[i]: the sibling of the node on the path to this coin
 *               at the i'th level from the bottom.
 *   direction[i]: "0" or "1" indicating whether that sibling is on the left.
 *       The "sibling" hashes correspond directly to the siblings in the
 *       SparseMerkleTree path.
 *       The "direction" keys the boolean directions from the SparseMerkleTree
 *       path, casted to string-represented integers ("0" or "1").
 */
 
template Spend(depth) {
    signal input digest;
    signal input nullifier;
    signal private input nonce;
    signal private input sibling[depth];
    signal private input direction[depth];

    // TODO

	component switch[depth];
	component hashes[depth + 1];
	
	hashes[0] = Mimc2();
	hashes[0].in0 <== nullifier;
	hashes[0].in1 <== nonce;
	for(var i=0; i <depth; i++)
	{
		switch[i] = SelectiveSwitch();
		switch[i].in0 <== hashes[i].out;
		switch[i].in1 <== sibling[i];
		switch[i].s <== direction[i];
		
		hashes[i+1] = Mimc2();
		hashes[i+1].in0 <== switch[i].out0;
		hashes[i+1].in1 <== switch[i].out1;
	}
	
	digest === hashes[depth].out;	
}
