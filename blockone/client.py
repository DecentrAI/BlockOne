# -*- coding: utf-8 -*-
"""

conda install -c anaconda pycrypto  

"""
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec, rsa, padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

from blockone import constants  as ct
from blockone.base import BlockOneBase
from blockone.chain import BlockOneChain
from blockone.transaction import BlockOneTransaction


class BlockOneClient(BlockOneBase):
  def __init__(self, 
               name, 
               family_name, 
               blockchain: BlockOneChain, 
               method=ct.ENC.EC,
               **kwargs):
    super(BlockOneClient, self).__init__(**kwargs)
    assert method in [ct.ENC.EC, ct.ENC.RSA]
    if isinstance(name, str):
      if ' ' in name:
        name = name.split(' ')
      else:
        name = [name]          
    if isinstance(family_name, str):
      family_name = [family_name]
    self.given_name = name
    self.family_name = family_name
    self.chain = blockchain
    self._method = method
    self.full_name = " ".join(self.given_name + [x.upper() for x in self.family_name])
    self._generate()
    return
  
  def update_chain(self, blockchain):
    self.chain = blockchain
    return
  
  
  def _generate(self):
    if self._method == ct.ENC.EC:
      self._private_key = self._generate_ec()
    else:
      self._private_key = self._generate_rsa()
    self._public_key = self._private_key.public_key()
    return

  
  def get_identity(self, as_message=False):
    if as_message:
      return self._public_key.public_bytes(
        encoding=Encoding.PEM, 
        format=PublicFormat.SubjectPublicKeyInfo,
        ).decode('utf-8')   
    data = self._public_key.public_bytes(Encoding.DER, PublicFormat.SubjectPublicKeyInfo)
    txt = self.binary_to_text(data)
    return txt
      
  
  @property
  def identity(self):
    return self.get_identity()
  
  
  @property
  def address(self):
    return ct.ENC.ADDRESS_PREFIX + self.get_identity()
    
    
    
  
  def sign(self, data, text=False, **kwargs):
    func, res = None, None
    if self._method == ct.ENC.EC:
      func = self.sign_ec
    elif self._method == ct.ENC.RSA:
      func = self.sign_rsa
    if func is not None:
      res = func(
          data=data,
          private_key=self._private_key,
          text=text,
          )
    return res

       
  def encrypt_rsa(self, msg):    
    if self._enc.lower() != 'rsa':
      self.P("Cannot encrypt/decrypt with '{}'".format(self._enc))
      return
    return self._public_key.encrypt(
      plaintext=bytes(msg, 'utf-8'), 
      padding=padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
        ),
      )
  
  
  def decrypt_rsa(self, enc_msg, decode=None):
    if self._enc.lower() != 'rsa':
      self.P("Cannot encrypt/decrypt with '{}'".format(self._enc))
      return
    res = self._private_key.decrypt(
      ciphertext=bytes(enc_msg, 'utf-8') if type(enc_msg) == str else enc_msg, 
      padding=padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
        ),
      )
    return res.decode(decode) if decode is not None else res
  
  
  def __repr__(self):
    res = "{}: {}, ADDR: {}, Pending: {}, Ballance: {}".format(
      self.__class__.__name__, self.full_name, self.address,
      len(self.get_unconfirmed()), 
      self.ballance
      )
    return res
  
  @property
  def ballance(self):
    ballance = 0
    for block in self.chain.chain:
      for dct_tran in block['transactions']:
        tran = BlockOneTransaction(**dct_tran)
        if self.address == tran.snd:
          ballance -= tran.data['val']
        elif self.address == tran.data['rcv']:
          ballance += tran.data['val']
    return ballance
  
  def get_unconfirmed(self):
    unconf = self.chain.get_unconfirmed(
      filter_address=self.address,
      data_subkey='rcv',
      data_value=self.address
      )
    return unconf
  
  def sign_transaction(self, tx:BlockOneTransaction):
    message = tx.to_message()
    text_sign, data = self.sign(message, text=True)
    vars(tx)[ct.TRAN.TXSIGN] = text_sign
    vars(tx)[ct.TRAN.SNDPK] = self.identity
    vars(tx)[ct.TRAN.METHOD] = self._method
    return text_sign


    
if __name__ == '__main__':
  chain = BlockOneChain()
  if True:
    andrei = BlockOneClient('Andrei Ionut', 'Damian', blockchain=chain)
  
    print(andrei)
    msg = "test de date" + 100*"*" + '!'
    if andrei._method == ct.ENC.RSA:
      enc = andrei.encrypt_rsa(msg)
      print('*****************************\nMesaj criptat:\n{}'.format(enc))
      dec_msg = andrei.decrypt_rsa(enc, decode='utf-8')
      print('*****************************\nMesaj decriptat:\n{}'.format(dec_msg))
      print("ALL OK." if msg == dec_msg else "FAILED ENC/DEC!")
    
    addr1 = andrei.address
    
    sign, _ = andrei.sign(msg, text=True)
    
    # sign = sign[:-1] + 'A'
    
    loaded_p = chain.text_to_binary(andrei.identity)
    p = serialization.load_der_public_key(loaded_p)
    bsign = chain.text_to_binary(sign)
    res = chain.verify(
      public_key=p,
      signature=bsign,
      data=msg,
      method=andrei._method
      )
    print(res)
    
    if False:
      from brute import AddrFinder
      finder = AddrFinder(addr1=addr1, nr_threads=5, nr_matches=30)
      finder.run()



  # test pki

  encoding = Encoding.DER # Encoding.X962
  enc_format = PublicFormat.SubjectPublicKeyInfo # PublicFormat.CompressedPoint
  pk = ec.generate_private_key(ec.SECP256K1)
  p = pk.public_key()
  tp = chain.binary_to_text(p.public_bytes(encoding=encoding, format=enc_format))
  print(tp)
  bp = chain.text_to_binary(tp)
  
  lp = serialization.load_der_public_key(bp)