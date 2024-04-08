# -*- coding: utf-8 -*-
"""

@created on: Tue Nov  9 09:02:10 2021
@created by: damia
"""

from collections import OrderedDict
from datetime import datetime
import json

import blockone.constants as ct
from blockone.base import BlockOneBase


class BlockOneTransaction(BlockOneBase):
  def __init__(self, 
               data, 
               snd,
               method='', 
               name='', **kwargs):
    super(BlockOneTransaction, self).__init__()
    assert isinstance(data, dict)
    assert isinstance(snd, str)
    self.time = self.get_timestamp()
    self.data = self.preprocess_data_dict(data)
    self.snd = snd    
    self._method = method
    return
  
  
  
  def get_timestamp(self):
    return datetime.now().strftime('%Y%m%d%H%M%S%f')   
  
  def to_dict_basic(self):    
    dct_res = OrderedDict({
      'snd' : self.snd, # sender extracted public address
      'data' : self.data, 
      'time': self.time,
      })
    return dct_res
  
  def to_message_basic(self):
    dct_res = self.to_dict_basic()
    return self._to_message(dct_res)
  
  
  def to_dict(self):
    dct_res = self.to_dict_basic()
    dct_res[ct.TRAN.TXHASH] = self._compute_hash(self._to_message(dct_res))
    return dct_res
  
  def to_message(self):
    dct_res = self.to_dict()      
    msg = self._to_message(dct_res)  
    return msg
  
  def show(self):
    print(self.to_message())    
  
  def __repr__(self):
    res = '{}\n'.format(self.__class__.__name__)
    res = res  + self.to_message()
    return res
  

  
  
if __name__ == '__main__':
  from blockone.client import BlockOneClient
  from blockone.chain import BlockOneChain
  chain = BlockOneChain()
  c1 = BlockOneClient(name='John', family_name='Doe', blockchain=chain)
  c2 = BlockOneClient(name='Jane', family_name='Doe', blockchain=chain)
  t = BlockOneTransaction(
    snd=c1.address, 
    data=dict(
      rcv=c2.address, 
      val=5
      )
    )
  ts, bs, m = c1.sign_transaction(tx=t)
  print(ts)
  

  res1, msg1 = chain.verify(data=m, signature=ts, public_key=c1.identity)
  print(msg1)
  ts_bad = ts[:-1] + 'A'
  res2, msg2 = chain.verify(data=m, signature=ts_bad, public_key=c1.identity)
  print(msg2)
    
  
