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
@created on: Tue Nov  9 09:06:47 2021
@created by: damia
"""

from blockone.transaction import BlockOneTransaction
from blockone.chain import BlockOneChain
from blockone.miner import BlockOneMiner
from blockone.wallet import BlockOneWallet
  
if __name__ == '__main__':
  chain = BlockOneChain()
  miner = BlockOneMiner(chain)
  
  user1 = 'Joe'
  wallet1 = BlockOneWallet(blockchain=chain, user=user1)
  user2 = 'Andrew'
  wallet2 = BlockOneWallet(blockchain=chain, user=user2)
  
  tran1 = BlockOneTransaction(
    snd=user1,
    rcv=user2,
    val=1,
    )
  chain.add_new_transaction(tran1)

  tran2 = BlockOneTransaction(
    snd=user1,
    rcv=user2,
    val=1,
    )
  chain.add_new_transaction(tran2)
  
  print(wallet1)
  print(wallet2)
  miner.mine()

  tran3 = BlockOneTransaction(
    snd=user1,
    rcv=user2,
    val=1,
    )  
  chain.add_new_transaction(tran3)

  print(wallet1)
  print(wallet2)

  miner.mine()

  print(wallet1)
  print(wallet2)

  tran4 = BlockOneTransaction(
    snd=user1,
    rcv=user2,
    val=1,
    )  
  chain.add_new_transaction(tran3)

  print(wallet1)
  print(wallet2)
