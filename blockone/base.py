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


class BlockOneBase:
  def __init__(self, **kwargs):
    self.name = ''
    self.log = kwargs.get('log')
    return  
  
  def P(self, msg):
    self.log.P(msg)


  def compute_hash(self):
    return self._compute_hash(self.to_message().encode())
  
  def _compute_hash(self, data):
    if isinstance(data, str):
      data = data.encode()
    if isinstance(data, dict):
      data = self._to_message(data).encode()
    return sha256(data).hexdigest()    

  def _to_message(self, data):
    if isinstance(data, dict) and type(data) != OrderedDict:
      data = OrderedDict(data)
      
    data = self.preprocess_data_dict(data)

    return json.dumps(
      data, 
      indent=4, 
      # sort_keys=True
      )
    
  def to_message(self):
    return self._to_message(self.to_dict())
  
  
  def to_dict(self):
    return OrderedDict(self.__dict__)
  
  
  def preprocess_data_dict(self, data):
    if isinstance(data, dict):
      # hard-coded encoding of binary keys
      for k,v in data.items():
        if isinstance(v, bytes):
          data[k] = v.decode()
    return data
    
  
    
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