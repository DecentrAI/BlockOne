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
@created on: Tue Nov  9 09:25:53 2021
@created by: damia
"""
from blockone.chain import BlockOneChain
from blockone.transaction import BlockOneTransaction

class BlockOneWallet:
  def __init__(self, blockchain: BlockOneChain, user):
    self.chain = blockchain
    self.user = user
    return

  @property
  def ballance(self):
    ballance = 0
    for block in self.chain.chain:
      for dct_tran in block.transactions:
        tran = BlockOneTransaction(**dct_tran)
        if self.user == tran.snd:
          ballance -= tran.val
        elif self.user == tran.rcv:
          ballance += tran.val
    return ballance
  
  def get_unconfirmed(self):
    unconf = self.chain.get_unconfirmed()
    return [x for x in unconf if x.snd == self.user or x.rcv == self.user]
    
  
  def __repr__(self):
    status = "Wallet of {}: transactions pending: {}. Ballance: {}".format(
      self.user,
      len(self.get_unconfirmed()), 
      self.ballance
      )
    return status