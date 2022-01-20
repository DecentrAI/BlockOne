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
@author: Lummetry.AI - AID
@project:
@description:

"""

CHAIN = 'chain'
UNCONF = 'unconfirmed_transactions'

class ENC:
  ADDRESS_SIZE = 40
  ADDRESS_PREFIX = 'add'

  KEY_SIZE = 2048
  PUBLIC_EXPONENT = 65537
  
  EC = 'ec'
  RSA = 'rsa'
  
  DIFFICULTY = 'difficulty'
  
  
class TRAN:
  GENESIS = 'Genesis'
  SND = 'snd'
  RCV = 'rcv'
  TXSIGN = 'tx_sign'
  TXHASH = 'tx_hash'
  VAL = 'val'
  DATA = 'data'
  SNDPK = '_sender_public_key'
  METHOD = '_method'
  EXTERNAL = [TXSIGN, SNDPK, METHOD, TXHASH]
  
class BLOCK:
  INDEX = 'index'
  HASH = 'block_hash'
  NONCE = 'nonce'
  PREV_HASH = 'previous_hash'
  TRANS = 'transactions'
  MINER = 'miner'
  EXTERNAL = [MINER, HASH]
