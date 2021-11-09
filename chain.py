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

import time
import json

from block import Block
from transaction import BlockOneTransaction



class BlockOneChain:
  def __init__(self, initial_difficulty=1):
    self.chain = []
    self.difficulty = initial_difficulty
    self.reset_transactions()
    self.create_genesys_block()
    return    
    
  
  def maybe_increment_difficulty(self):
    self.difficulty += 1
    return
  
  
  def get_timestamp(self):
    return time.time()
  
  
  def get_unconfirmed(self, as_dicts=False):
    if as_dicts:
      return [x.__dict__ for x in self.unconfirmed_transactions]
    else:
      return [x for x in self.unconfirmed_transactions]
  
  
  def create_genesys_block(self):
    gen_blk = Block(
      index=0,
      transactions=[],
      timestamp=time.time(),
      previous_hash="0",
      )
    gen_blk.hash = gen_blk.compute_hash()
    self.chain.append(gen_blk)
    return
  
  
  def add_new_transaction(self, transaction, force_dict=False):
    if isinstance(transaction, (object,)) and force_dict:
      dct_trans = transaction.__dict__
    else:
      dct_trans = transaction
    self.unconfirmed_transactions.append(dct_trans)
    
  def reset_transactions(self):
    self.unconfirmed_transactions = []
  
  
  @property
  def last_block(self):
    return self.chain[-1]

  
  def is_difficulty_valid(self, block: Block, proof: str):
    required_start = '0' * self.difficulty
    is_start_valid = proof.startswith(required_start)
    return is_start_valid
  
  
  def is_proof_of_work_valid(self, block: Block, proof: str):
    is_hash_valid = proof == block.compute_hash()
    is_diff_valid = self.is_difficulty_valid(block=block, proof=proof)
    return is_diff_valid and is_hash_valid
  
  
  def add_block(self, block : Block, proof):
    previous_hash = self.last_block.hash
    if previous_hash != block.previous_hash:
      return False
    
    if not self.is_proof_of_work_valid(block=block, proof=proof):
      return False
    
    block.hash = proof
    self.chain.append(block)
    self.maybe_increment_difficulty()
    return True
      
  
  def __repr__(self):
    chain = [x.__dict__ for x in self.chain]
    return json.dumps(chain, indent=4)
  
  
    
