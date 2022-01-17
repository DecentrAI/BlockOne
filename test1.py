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
from blockone.client import BlockOneClient
  
if __name__ == '__main__':
  chain = BlockOneChain()

  client1 = BlockOneClient(blockchain=chain, name='Andrew', family_name='')
  chain.create_genesys_block(client1.address)

  miner = BlockOneMiner(chain)
  
  client2 = BlockOneClient(blockchain=chain, name='Joe', family_name='')
  
  print("* adding good tran")
  tx1 = BlockOneTransaction(    
    snd=client1.address,
    data=dict(
      rcv=client2.address,
      val=1,
      )
    )
  sign1 = client1.sign_transaction(tx1)
  chain.add_new_transaction(tx1)

  
  print("* adding good tran")
  tx2 = BlockOneTransaction(
    snd=client1.address,
    data=dict(
      rcv=client2.address,
      val=1,
      )
    )
  sign2 = client1.sign_transaction(tx2)
  chain.add_new_transaction(tx2)
  
  print(client1)
  print(client2)
  miner.mine()
  print(client1)
  print(client2)
  
  print("* adding bad tran")
  tx3 = BlockOneTransaction(
    snd=client1.address,
    data=dict(
      rcv=client2.address,
      val=1,
      ),
    name='bad'
    )  
  # now we forge the validation
  tx3._sender_public_key = tx2._sender_public_key
  tx3.tx = tx2.tx 
  tx3._method = tx2._method 
  # now we ask the chain to add the transaction for the miners to mine
  chain.add_new_transaction(tx3)

  print(client1)
  print(client2)
  miner.mine()
  print(client1)
  print(client2)

  print("* adding good tran")
  tx4 = BlockOneTransaction(
    snd=client1.address,
    data=dict(
      rcv=client2.address,
      val=1,
      )
    )  
  sign4 = client1.sign_transaction(tx4)
  chain.add_new_transaction(tx4)

  print(client1)
  print(client2)
  
  chain.dump_blockchain()

  miner.mine()
  print(client1)
  print(client2)
  print(chain)
  
