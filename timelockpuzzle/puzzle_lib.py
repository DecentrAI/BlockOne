# -*- coding: utf-8 -*-
"""
Copyright 2019-2021 Lummetry.AI (Knowledge Investment Group SRL). All Rights Reserved.


* NOTICE:  All information contained herein is, and remains
* the property of Knowledge Investment Group SRL.  
* The intellectual and technical concepts contained
* herein are proprietary to Knowledge Investment Group SRL
* and may be covered by Romanian and Foreign Patents,
* patents in process, and are protected by trade secret or copyright law.
* Dissemination of this information or reproduction of this material
* is strictly forbidden unless prior written permission is obtained
* from Knowledge Investment Group SRL.


@copyright: Lummetry.AI
@author: Lummetry.AI
@project: 
@description:
@created on: Fri Sep 30 10:30:51 2022
@created by: damia
"""


import os
import sys
import timeit


from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa


def _successive_squares(base: int, mod: int, length: int) -> [int]:
    table = [base % mod]
    prev = base % mod
    for n in range(1, length):
        squared = prev**2 % mod
        table.append(squared)
        prev = squared
    return table

def _fast_exponentiation(n: int, g: int, x: int) -> int:
    # reverses binary string
    binary = bin(x)[2:][::-1]
    squares = _successive_squares(g, n, len(binary))
    # keeps positive powers of two
    factors = [tup[1] for tup in zip(binary, squares) if tup[0] == '1']
    acc = 1
    for factor in factors:
        acc = acc * factor % n
    return acc


def encrypt(message: bytes, seconds: int, squarings_per_second: int):
    if not seconds or not squarings_per_second:
        raise AssertionError

    # hard code safe exponent to use
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    # see RSA for security specifications
    p, q = private_key.private_numbers().p, private_key.private_numbers().q
    n = private_key.public_key().public_numbers().n
    phi_n = (p - 1) * (q - 1)

    # Fernet is an asymmetric encryption protocol using AES
    key = Fernet.generate_key()
    key_int = int.from_bytes(key, sys.byteorder)
    cipher_suite = Fernet(key)

    # Vote Encryption
    encrypted_message = cipher_suite.encrypt(message)

    # Pick safe, pseudo-random a where 1 < a < n
    # Alternatively, we could use a = 2
    a = int.from_bytes(os.urandom(32), sys.byteorder) % n + 1

    # Key Encryption
    t = seconds * squarings_per_second
    e = 2**t % phi_n
    b = _fast_exponentiation(n, a, e)

    encrypted_key = (key_int % n + b) % n
    return p, q, n, a, t, encrypted_key, encrypted_message, key_int


def decrypt(n: int, a: int, t: int, enc_key: int, enc_message: int) -> bytes:
    # Successive squaring to find b
    # We assume this cannot be parallelized
    b = a % n
    for i in range(t):
        b = b**2 % n
    dec_key = (enc_key - b) % n

    # Retrieve key, decrypt message
    key_bytes = int.to_bytes(dec_key, length=64, byteorder=sys.byteorder)
    cipher_suite = Fernet(key_bytes)
    return cipher_suite.decrypt(enc_message)


if __name__ == '__main__':
    # We use the main function to time the accuracy of the decrypt function
    # Import the methods to use as-is
    if len(sys.argv) != 4:
        print('Please provide t, s')
    arg_t, arg_s, arg_repeats = sys.argv[1], sys.argv[2], sys.argv[3]
    print("t =", arg_t)
    print("s =", arg_s)

    p, q, n, a, t, encrypted_key, encrypted_message, original_key = encrypt(
        "This is a vote for Myrto".encode(),
        int(arg_t),
        int(arg_s)
    )

    print('Decrypting')
    # TODO: make separate script for measuring this
    # time it provides an accurate timing function with disabled garbage collecting
    # https://docs.python.org/3/library/timeit.html
    print(timeit.repeat(
        'print(decrypt(n, a, t, encrypted_key, encrypted_message))',
        globals=globals(),
        repeat=int(arg_repeats),
        number=1)
    )