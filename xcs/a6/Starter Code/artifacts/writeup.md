Name: []

## Question 1

In the following code-snippet from `Num2Bits`, it looks like `sum_of_bits`
might be a sum of products of signals, making the subsequent constraint not
rank-1. Explain why `sum_of_bits` is actually a _linear combination_ of
signals.

```
        sum_of_bits += (2 ** i) * bits[i];
```

## Answer 1

This is a simple calculation of the decimal value given a binary representation of the original number in bits vector where the least significant bit is on position 0 of the vector and each individual position contains value 0  or 1. Basically each individual iteration sets to 0 or 1 the particular "bit" of the original number starting from the least important.


## Question 2

Explain, in your own words, the meaning of the `<==` operator.

## Answer 2

The operator `<==` generates two sequential operations, one of a immutable assignment and another of "assertion" if the left signal matches the value of the right formula/value.

## Question 3

Suppose you're reading a `circom` program and you see the following:

```
    signal input a;
    signal input b;
    signal input c;
    (a & 1) * b === c;
```

Explain why this is invalid.

## Answer 3

This is invalid because (a & 1) is not a liniar combination of the signals. The === requires a quadratic expresion and although `a'*b === c` is valid `a'` is not a valid expresion.
