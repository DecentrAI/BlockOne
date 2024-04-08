# -*- coding: utf-8 -*-
"""

@created on: Mon Nov  8 09:21:31 2021
@created by: damia
"""
import json
from datetime import datetime

from blockone.base import BlockOneBase


class Block(BlockOneBase):
  def __init__(self, 
               index,
               block_name=None,
               transactions=[],
               previous_hash="",
               nonce=0,
               timestamp=None,
               date=None,
               ):
    super(Block, self).__init__()
    self.index = index
    if block_name is None:
      block_name = 'B' + str(index)
    self.block_name = block_name
    self.transactions = transactions
    if date is None:
      date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    self.date = date
    if timestamp is None:
      timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f') 
    self.timestamp = str(timestamp)
    self.previous_hash = previous_hash
    self.nonce = nonce
    return
    
  
  def __repr__(self):
    res = '{}\n'.format(self.__class__.__name__)
    res = res  + self.to_message()
    return res
  
  
  @property
  def block_size(self):
    return len(self.transactions)
  
    