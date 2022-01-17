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
@created on: Mon Nov  8 09:25:35 2021
@created by: damia

roughly inspired from https://www.activestate.com/blog/how-to-build-a-blockchain-in-python/#:~:text=A%20Python%20blockchain%20is%20simply,create%20a%20blockchain%20in%20Python%3A&text=Encrypt%20each%20block%20with%20a%20cryptographic%20hash%20function%20to%20ensure%20immutability
"""

import json
import binascii
import cryptography
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from datetime import datetime


from blockone.base import BlockOneBase
from blockone.block import Block
from blockone.transaction import BlockOneTransaction
import blockone.constants as ct



class BlockOneChain(BlockOneBase):
  def __init__(self, initial_difficulty=1):
    super(BlockOneChain, self).__init__()
    self.chain = []
    self.difficulty = initial_difficulty
    self.reset_transactions()
    self.name = self.__class__.__name__
    self.P("Initializing on cryptography v.{}".format(cryptography.__version__))
    return    
    
  
  def maybe_increment_difficulty(self):
    self.difficulty += 1
    return
  
  
  def get_timestamp(self):
    return datetime.now().strftime('%Y%m%d%H%M%S%f') 
  
  
  def get_unconfirmed(self, filter_address=None, data_subkey=None, data_value=None):
    res = [x for x in self.unconfirmed_transactions]
    if filter_address is not None:
      res = [x for x in res if x.snd == filter_address]
    if data_subkey is not None:
      res = [x for x in res if x.data[data_subkey] == data_value]
    return [x.to_dict() for x in res]
    
  
  
  def create_genesys_block(self, client_zero):
    tx = BlockOneTransaction(
      snd='Genesis',
      data=dict(
        rcv=client_zero,
        val=500,
        )
      )
    gen_blk = Block(
      index=0,
      block_name='Genesis',
      transactions=[tx.to_dict()],
      timestamp=self.get_timestamp(),
      previous_hash="0",
      )
    gen_blk.hash = gen_blk.compute_hash()
    self.chain.append(gen_blk)
    return
  
  
  def add_new_transaction(self, transaction, force_dict=False):
    check_ok, msg = self.verify_transaction(
        tx=transaction, 
        )
    if not check_ok:
      self.P("Transaction failed: {}".format(msg))
      return
      
    if isinstance(transaction, (object,)) and force_dict:
      dct_trans = transaction.to_dict()
    else:
      dct_trans = transaction
    self.unconfirmed_transactions.append(dct_trans)
    self.P("Transaction added succesfully to pending transactions. Signature: {}/{}".format(check_ok, msg))
    return
    
  def reset_transactions(self):
    self.unconfirmed_transactions = []
  
  
  @property
  def last_block(self):
    return self.chain[-1]
  
  @property
  def chain_size(self):
    return len(self.chain)

  
  def is_difficulty_valid(self, block: Block, proof: str):
    required_start = '0' * self.difficulty
    is_start_valid = proof.startswith(required_start)
    return is_start_valid
  
  
  def is_proof_of_work_valid(self, block: Block, proof: str):
    is_hash_valid = proof == block.compute_hash()
    is_diff_valid = self.is_difficulty_valid(block=block, proof=proof)
    return is_diff_valid and is_hash_valid
  
  
  def add_block(self, block : Block, proof, miner):
    previous_hash = self.last_block.hash
    if previous_hash != block.previous_hash:
      return False
    
    if not self.is_proof_of_work_valid(block=block, proof=proof):
      return False
    else:
      self.P("PoW valid from miner {}".format(miner))
    
    block.hash = proof
    block.miner = miner
    self.chain.append(block)
    self.maybe_increment_difficulty()
    return True

  
  def dump_blockchain(self):
    barsize = 110
    sz = self.chain_size
    self.P("=" * barsize)
    self.P("Dumping full blockchain with {} blocks".format(sz))
    for bidx in range(sz):
      blk = self.chain[bidx]
      self.P("  Block #{} '{}':".format(blk.index,blk.block_name))
      for tidx in range(blk.block_size):
        tx = blk.transactions[tidx]
        snd = tx[ct.TRAN.SND]
        data = tx[ct.TRAN.DATA]
        self.P("    FROM: {}  DATA: {}".format(snd, data))
    self.P("-" * barsize)
    self.P("  Unconfirmed transactions:")
    utxs = self.get_unconfirmed()
    for uidx in range(len(utxs)):
      utx = utxs[uidx]
      snd = utx[ct.TRAN.SND]
      data = utx[ct.TRAN.DATA]
      self.P("    ** FROM: {}  DATA: {}".format(snd, data))
      
    return
  
  def verify_transaction(self, tx):
    # first we extract needed info from transaction
    if isinstance(tx, BlockOneTransaction):
      tx_sign = tx.tx
      tx_snd = tx.snd
      tx_dump = tx.to_message()
      tx_method = tx._method
      tx_snd_pk = tx._sender_public_key
    elif isinstance(tx, dict):
      tx_sign = tx[ct.TRAN.TX]
      tx_snd = tx[ct.TRAN.SND]
      dct_new = {k:v for k,v in tx.items() if k not in ct.TRAN.EXTERNAL}
      tx_dump = self._to_message(dct_new)
      tx_snd_pk = tx[ct.TRAN.SNDPK]
      tx_method = tx[ct.TRAN.METHOD]
    # we compare the sender address with the public key  
    addr1 = ct.ENC.ADDRESS_PREFIX + tx_snd_pk[-ct.ENC.ADDRESS_SIZE:]
    if  addr1 != tx_snd:
      return False, "Verification failed. Forged address/key: SND: '{}' vs SND_PK: '{}'".format(
        tx_snd, addr1)
    
    # now we verify the signature
    res = self.verify(
      data=tx_dump,
      signature=tx_sign,
      public_key=tx_snd_pk,
      method=tx_method,
      )    
    return res
      
  
  def __repr__(self):
    res = '{}\n'.format(self.__class__.__name__)
    chain = [x.__dict__ for x in self.chain]
    res = res  + json.dumps(chain, indent=4)
    return res
  
  
    
