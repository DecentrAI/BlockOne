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
@created on: Tue Nov  9 09:02:10 2021
@created by: damia
"""
from collections import OrderedDict
from datetime import datetime
import json

from blockone.client import BlockOneClient
import blockone.constants as ct


class BlockOneTransaction:
  def __init__(self, snd : BlockOneClient, rcv, val):
    self.time = datetime.now()
    self.snd = snd
    self.rcv = rcv
    self.val = val
    return
  
  def to_message(self):
    if self.snd == ct.TRAN.GENESIS:
      identity = ct.TRAN.GENESIS
    else:
      identity = self.snd.identity
    dct_res = OrderedDict({
      'snd' : identity, # sender extracted public key identity
      'rcv' : self.rcv, # receiver public key
      'val' : self.val,
      'time': str(self.time),
      })
    return json.dumps(dct_res)
  
  def sign(self):
    message = self.to_message()
    signature, data = self.snd.sign(message)
    return signature, data
  
  
  
  
if __name__ == '__main__':
  c1 = BlockOneClient(name='John', family_name='Doe')
  c2 = BlockOneClient(name='Jane', family_name='Doe')
  t = BlockOneTransaction(
    snd=c1, 
    rcv=c2.identity, 
    val=5
    )
  s, m = t.sign()
  print(s)
  
  c1.verify(data=m, signature=s)
    
  
