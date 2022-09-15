# -*- coding: utf-8 -*-
"""
Copyright 2017-2021 Lummetry.AI (Knowledge Investment Group SRL). All Rights Reserved.
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
@author: Lummetry.AI - AID
@project:
@description:

"""

import json
import binascii
import base64
from hashlib import sha256
from collections import OrderedDict


from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec, rsa, padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

import blockone.constants as ct

## RIPEMD160

# Message schedule indexes for the left path.
ML = [
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
    7, 4, 13, 1, 10, 6, 15, 3, 12, 0, 9, 5, 2, 14, 11, 8,
    3, 10, 14, 4, 9, 15, 8, 1, 2, 7, 0, 6, 13, 11, 5, 12,
    1, 9, 11, 10, 0, 8, 12, 4, 13, 3, 7, 15, 14, 5, 6, 2,
    4, 0, 5, 9, 7, 12, 2, 10, 14, 1, 3, 8, 11, 6, 15, 13
]

# Message schedule indexes for the right path.
MR = [
    5, 14, 7, 0, 9, 2, 11, 4, 13, 6, 15, 8, 1, 10, 3, 12,
    6, 11, 3, 7, 0, 13, 5, 10, 14, 15, 8, 12, 4, 9, 1, 2,
    15, 5, 1, 3, 7, 14, 6, 9, 11, 8, 12, 2, 10, 0, 4, 13,
    8, 6, 4, 1, 3, 11, 15, 0, 5, 12, 2, 13, 9, 7, 10, 14,
    12, 15, 10, 4, 1, 5, 8, 7, 6, 2, 13, 14, 0, 3, 9, 11
]

# Rotation counts for the left path.
RL = [
    11, 14, 15, 12, 5, 8, 7, 9, 11, 13, 14, 15, 6, 7, 9, 8,
    7, 6, 8, 13, 11, 9, 7, 15, 7, 12, 15, 9, 11, 7, 13, 12,
    11, 13, 6, 7, 14, 9, 13, 15, 14, 8, 13, 6, 5, 12, 7, 5,
    11, 12, 14, 15, 14, 15, 9, 8, 9, 14, 5, 6, 8, 6, 5, 12,
    9, 15, 5, 11, 6, 8, 13, 12, 5, 12, 13, 14, 11, 8, 5, 6
]

# Rotation counts for the right path.
RR = [
    8, 9, 9, 11, 13, 15, 15, 5, 7, 7, 8, 11, 14, 14, 12, 6,
    9, 13, 15, 7, 12, 8, 9, 11, 7, 7, 12, 7, 6, 15, 13, 11,
    9, 7, 15, 11, 8, 6, 6, 14, 12, 13, 5, 14, 13, 13, 7, 5,
    15, 5, 8, 11, 14, 14, 6, 14, 6, 9, 12, 9, 12, 5, 15, 8,
    8, 5, 12, 9, 12, 5, 14, 6, 8, 13, 6, 5, 15, 13, 11, 11
]

# K constants for the left path.
KL = [0, 0x5a827999, 0x6ed9eba1, 0x8f1bbcdc, 0xa953fd4e]

# K constants for the right path.
KR = [0x50a28be6, 0x5c4dd124, 0x6d703ef3, 0x7a6d76e9, 0]


def fi(x, y, z, i):
    """The f1, f2, f3, f4, and f5 functions from the specification."""
    if i == 0:
        return x ^ y ^ z
    elif i == 1:
        return (x & y) | (~x & z)
    elif i == 2:
        return (x | ~y) ^ z
    elif i == 3:
        return (x & z) | (y & ~z)
    elif i == 4:
        return x ^ (y | ~z)
    else:
        assert False


def rol(x, i):
    """Rotate the bottom 32 bits of x left by i bits."""
    return ((x << i) | ((x & 0xffffffff) >> (32 - i))) & 0xffffffff


def compress(h0, h1, h2, h3, h4, block):
    """Compress state (h0, h1, h2, h3, h4) with block."""
    # Left path variables.
    al, bl, cl, dl, el = h0, h1, h2, h3, h4
    # Right path variables.
    ar, br, cr, dr, er = h0, h1, h2, h3, h4
    # Message variables.
    x = [int.from_bytes(block[4*i:4*(i+1)], 'little') for i in range(16)]

    # Iterate over the 80 rounds of the compression.
    for j in range(80):
        rnd = j >> 4
        # Perform left side of the transformation.
        al = rol(al + fi(bl, cl, dl, rnd) + x[ML[j]] + KL[rnd], RL[j]) + el
        al, bl, cl, dl, el = el, al, bl, rol(cl, 10), dl
        # Perform right side of the transformation.
        ar = rol(ar + fi(br, cr, dr, 4 - rnd) + x[MR[j]] + KR[rnd], RR[j]) + er
        ar, br, cr, dr, er = er, ar, br, rol(cr, 10), dr

    # Compose old state, left transform, and right transform into new state.
    return h1 + cl + dr, h2 + dl + er, h3 + el + ar, h4 + al + br, h0 + bl + cr


def ripemd160(data):
    """Compute the RIPEMD-160 hash of data."""
    # Initialize state.
    state = (0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476, 0xc3d2e1f0)
    # Process full 64-byte blocks in the input.
    for b in range(len(data) >> 6):
        state = compress(*state, data[64*b:64*(b+1)])
    # Construct final blocks (with padding and size).
    pad = b"\x80" + b"\x00" * ((119 - len(data)) & 63)
    fin = data[len(data) & ~63:] + pad + (8 * len(data)).to_bytes(8, 'little')
    # Process final blocks.
    for b in range(len(fin) >> 6):
        state = compress(*state, fin[64*b:64*(b+1)])
    # Produce output.
    return b"".join((h & 0xffffffff).to_bytes(4, 'little') for h in state)
  
# END ## RIPEMD160  

class BlockOneBase:
  def __init__(self, **kwargs):
    self.name = ''
    self.log = kwargs.get('log')
    return  
  
  def P(self, msg):
    self.log.P(msg)


  @staticmethod
  def preprocess_data_dict(data):
    if isinstance(data, dict):
      # hard-coded encoding of binary keys
      for k,v in data.items():
        if isinstance(v, bytes):
          data[k] = v.decode()
    return data


  @classmethod
  def _compute_hash(cls, data):
    if isinstance(data, dict):
      data = cls._to_message(data).encode()
    if isinstance(data, str):
      data = data.encode()      
    if not isinstance(data, bytes):
      data = str(data).encode()
      
    h160 = ripemd160(sha256(data).digest())
    return binascii.hexlify(h160).decode()

  @classmethod
  def _to_message(data):
    if isinstance(data, dict) and type(data) != OrderedDict:
      data = OrderedDict(data)
      
    data = BlockOneBase.preprocess_data_dict(data)

    return json.dumps(
      data, 
      indent=4, 
      # sort_keys=True
      )

  def compute_hash(self):
    return self._compute_hash(self.to_message().encode())
  
    
  def to_message(self):
    return self._to_message(self.to_dict())
  
  
  def to_dict(self):
    return OrderedDict(self.__dict__)
  
    
  
    
  def sign_rsa(self, data, private_key, text=False):
    data = data if type(data) == bytes else bytes(str(data), 'utf-8')
    signature = private_key.sign(
      data=data,
      padding=padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
        ),
      algorithm=hashes.SHA256()
      )
    txt_signature = self.binary_to_text(signature)
    return txt_signature, data if text else signature, data
  
  
  def binary_to_text(self, data, method='base64'):
    assert isinstance(data, bytes)
    if method == 'base64':
      txt = base64.b64encode(data).decode()
    else:
      txt = binascii.hexlify(data).decode()
    return txt
  
  def text_to_binary(self, text, method='base64'):
    assert isinstance(text, str)
    if method == 'base64':
      data = base64.b64decode(text)
    else:
      data = binascii.unhexlify(text)
    return data
    
  
  def sign_ec(self, data, private_key, text=False):
    data = data if type(data) == bytes else bytes(str(data), 'utf-8')
    signature = private_key.sign(
      data=data,
      signature_algorithm=ec.ECDSA(hashes.SHA256())
      )
    txt_signature = self.binary_to_text(signature)
    return (txt_signature, data) if text else (signature, data)
  
  
  def verify_rsa(self, public_key, signature, data):
    public_key.verify(
      signature=signature,
      data=data,
      padding=padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
        ),
      algorithm=hashes.SHA256()
      )    
    return True
  
    
  def verify_ec(self, public_key, signature, data):
    public_key.verify(signature, data, ec.ECDSA(hashes.SHA256()))
    return True
  
  
  def verify(self, public_key, signature, data, method):
    res = False
    msg = 'Fail!'
    if isinstance(signature, str):
      signature = self.text_to_binary(signature)
    
    if isinstance(public_key,str):
      bpublic_key = self.text_to_binary(public_key)
      public_key = serialization.load_der_public_key(bpublic_key)
      
    if isinstance(data, str):
      data = data.encode()
    
    try:
      if method == ct.ENC.EC:
        res = self.verify_ec(public_key, signature, data)
      elif method == ct.ENC.RSA:
        res = self.verify_rsa(public_key, signature, data)
      else:
        raise ValueError('Invalid method!')
      msg = '{} verification OK.'.format(method.upper())
    except Exception as exp:
      res = False
      err = str(exp)
      if len(err) == 0:
        err = exp.__class__.__name__
      msg = '{} verification FAILED. Reason: {}'.format(method.upper(), err)
    return res, msg
    
  
  def _generate_rsa(self):
    private_key = rsa.generate_private_key(
      public_exponent=ct.ENC.PUBLIC_EXPONENT,
      key_size=ct.ENC.KEY_SIZE,
      )
    return private_key
  
  
  def _generate_ec(self):
    private_key = ec.generate_private_key(ec.SECP256K1)
    return private_key
  
if __name__ == '__main__':
  v = 1
  h = BlockOneBase._compute_hash(v)
  print(h)
  
  