# -*- coding: utf-8 -*-
"""

"""

CHAIN = 'chain'
UNCONF = 'unconfirmed_transactions'

class ENC:
  ADDRESS_SIZE = 40
  ADDRESS_PREFIX = 'boxaddr'

  RSA_KEY_SIZE = 2048
  RSA_PUBLIC_EXPONENT = 65537
  
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
