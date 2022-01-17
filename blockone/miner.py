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
@created on: Tue Nov  9 09:01:03 2021
@created by: damia
"""
from time import time

from blockone.block import Block
from blockone.chain import BlockOneChain
from blockone.base import BlockOneBase

class BlockOneMiner(BlockOneBase):
  def __init__(self, blockchain: BlockOneChain, name='Miner0'):
    super(BlockOneMiner, self).__init__()
    self.chain = blockchain
    self.timings = []
    self.name = name
    return
  
  
  def proof_of_work(self, block: Block):
    block.nonce = 0
    computed_hash = block.compute_hash()
    while not self.chain.is_difficulty_valid(block=block, proof=computed_hash):
      block.nonce += 1
      computed_hash = block.compute_hash()
    return computed_hash

  
  def mine(self):
    blockchain = self.chain
    if not len(blockchain.unconfirmed_transactions) > 0:
      self.P("No transactions pending thus no block to generate.")
      return False
    self.P("Mining...")
    t_start = time()
    
    new_block = Block(
      index=blockchain.last_block['index'] + 1,
      transactions=blockchain.get_unconfirmed(),
      timestamp=blockchain.get_timestamp(),
      previous_hash=blockchain.last_block['block_hash'],
      )
    proof = self.proof_of_work(block=new_block)    
    
    blockchain.add_block(block=new_block, proof=proof, miner=self.name)
    blockchain.reset_transactions()
    self.timings.append(time() - t_start)
    self.P("Done mining in {:.4f}s.".format(self.timings[-1]))
    return new_block.index
  