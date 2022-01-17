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
      date = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
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
  
    