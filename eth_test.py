# -*- coding: utf-8 -*-
"""
Copyright 2017-2021 Lummetry.AI (Knowledge Investment Group SRL). All Rights Reserved.
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
@author: Lummetry.AI - AID
@project:
@description:

"""
import os

# os.environ["WEB3_INFURA_PROJECT_ID"] = "81f3ba2b95ff4056bb899598f6170f33"
# os.environ["WEB3_INFURA_API_SECRET"] = "709448d12b3b481ab820aba0ccbdb77f"

import web3
from web3 import Web3
# from web3.auto.infura import w3# 

if __name__ == '__main__':
  w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/81f3ba2b95ff4056bb899598f6170f33'))
  is_conn = w3.isConnected() 
  print("Web3 ver.{} is {}".format(
    web3.__version__, "connected" if is_conn else "NOT connected"))
  if is_conn:
    bal = w3.fromWei(
      w3.eth.getBalance(w3.toChecksumAddress('0x563f7d4ab22d603ff931233a338333a8b125b468')), 
      'ether'
      )
    print("Ballance: {} ETH".format(bal))
  