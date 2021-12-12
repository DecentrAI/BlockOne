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
@author: Lummetry.AI - AID
@project:
@description:
  
conda install -c anaconda pycrypto  

"""
import binascii
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

from blockone import constants  as ct

class BlockOneClient:
  def __init__(self, name, family_name):
    if isinstance(name, str):
      if ' ' in name:
        name = name.split(' ')
      else:
        name = [name]          
    if isinstance(family_name, str):
      family_name = [family_name]
    self.name = name
    self.family_name = family_name
    self.full_name = " ".join(self.name + [x.upper() for x in self.family_name])
    self._generate()
    return
  
  
  def _generate(self):
    self._private_key = rsa.generate_private_key(
      public_exponent=ct.ENC.PUBLIC_EXPONENT,
      key_size=ct.ENC.KEY_SIZE,
      )
    self._public_key = self._private_key.public_key()
  
  
  @property
  def identity(self):
    return self._public_key.public_bytes(
      encoding=Encoding.PEM, 
      format=PublicFormat.SubjectPublicKeyInfo
      ).decode('utf-8')
  
  
  def sign(self, data):
    data = data if type(data) == bytes else bytes(str(data), 'utf-8')
    signature = self._private_key.sign(
      data=data,
      padding=padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
        ),
      algorithm=hashes.SHA256()
      )
    return signature, data    
  
  def verify(self, data, signature):
    self._public_key.verify(
      signature=signature,
      data=data,
      padding=padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
        ),
      algorithm=hashes.SHA256()
      )    
  
  
  
  def encrypt(self, msg):    
    return self._public_key.encrypt(
      plaintext=bytes(msg, 'utf-8'), 
      padding=padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
        ),
      )
  
  
  def decrypt(self, enc_msg):
    return self._private_key.decrypt(
      ciphertext=bytes(enc_msg, 'utf-8') if type(enc_msg) == str else enc_msg, 
      padding=padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
        ),
      )
  
  
  def __repr__(self):
    res = "{}: {}, public key:\n{}".format(
      self.__class__.__name__, self.full_name, self.identity)
    return res
    
    
    
if __name__ == '__main__':
  
  Gigi = BlockOneClient('Andrei Ionut', 'Damian')
  print(Gigi)
  
  enc = Gigi.encrypt("test de criptare " + 100*"*")
  print(enc)
  print(Gigi.decrypt(enc).decode('utf-8'))
  
  
    
  