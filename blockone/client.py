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
  
  
  def get_identity(self, as_pki=False):
    if as_pki:
      return self._public_key.public_bytes(
        encoding=Encoding.PEM, 
        format=PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')
    else:
      return binascii.hexlify(self._public_key.public_bytes(Encoding.DER, PublicFormat.PKCS1)).decode('ascii')
      
  
  @property
  def identity(self):
    return self.get_identity(as_pki=True)
  
  @property
  def address(self):
    return self.get_identity(as_pki=False)[:ct.ENC.ADDRESS_SIZE]
  
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
    res = "{}: {}, ADDR: {}".format(
      self.__class__.__name__, self.full_name, self.address)
    return res
    
  
  
  
    
    
if __name__ == '__main__':
  import threading
  import time
  from collections import deque
  
  def match(a1, a2):
    addr_len = len(a1)
    trues = [a1[i] == a2[i] for i in range(addr_len)]
    return sum(trues)
  
  class AddrFinder:
    def __init__(self, addr1, nr_threads, nr_matches):
      self.addr1 = addr1
      self.nr_threads = nr_threads  
      self._counter = 0
      self._nr_matches = nr_matches
      self.found = False
      self.msgs = deque(maxlen=100)
      self.stats = {}
      return
    
    def msg(self, s):
      self.msgs.append(s)
      return
    
    def run(self):
      print("Trying to brute-force find similar address with {}/{} matches".format(
        self._nr_matches, len(self.addr1)))
      for thr in range(self.nr_threads):
        job = threading.Thread(target=self._job, kwargs={'id_job':thr+1})
        job.start()
      while not self.found:
        time.sleep(1)        
        print('\rStatus @ {}: {}\r'.format(self._counter, self.stats), flush=True, end='')
        if len(self.msgs) > 0:
          print(self.msgs.popleft())
        
        
    def _job(self, id_job=0):
      local_counter = 0
      while not self.found:
        self._counter += 1
        local_counter += 1
        clnt = BlockOneClient('**', '*')
        a2 = clnt.address
        matches = match(self.addr1, a2)
        if matches >= self._nr_matches:
          self.found = True
          self.msg('\nThread {} found match at glocal/local iter {}/{}: {} vs {}'.format(
            id_job, self._counter, local_counter, self.addr1, a2))
        self.stats[id_job] = local_counter
      return
        
  
  andrei = BlockOneClient('Andrei Ionut', 'Damian')
  print(andrei)
  
  enc = andrei.encrypt("test de criptare " + 100*"*" + '!')
  print('*****************************\nMesaj criptat:\n{}'.format(enc))
  dec_msg = andrei.decrypt(enc).decode('utf-8')
  print('*****************************\nMesaj decriptat:\n{}'.format(dec_msg))
  
  addr1 = andrei.address
  finder = AddrFinder(addr1=addr1, nr_threads=5, nr_matches=30)
  finder.run()
