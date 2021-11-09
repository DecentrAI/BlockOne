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
from hashlib import sha256
from datetime import datetime


class Block:
  def __init__(self, 
               index,
               transactions,
               timestamp,
               previous_hash,
               nonce=0,
               ):
    self.index = index
    self.transactions = transactions
    self.timestamp = timestamp
    self.date = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    self.previous_hash = previous_hash
    self.nonce = nonce
    return
    
  
  def __repr__(self):
    str_obj = json.dumps(self.__dict__, indent=4, sort_keys=True)
    return str_obj
        
  
  def compute_hash(self):
    return sha256(str(self).encode()).hexdigest()
  
    