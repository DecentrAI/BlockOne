# -*- coding: utf-8 -*-
"""

@created on: Mon Nov  8 09:25:35 2021
@created by: damia

roughly inspired from https://www.activestate.com/blog/how-to-build-a-blockchain-in-python/#:~:text=A%20Python%20blockchain%20is%20simply,create%20a%20blockchain%20in%20Python%3A&text=Encrypt%20each%20block%20with%20a%20cryptographic%20hash%20function%20to%20ensure%20immutability
"""

import json
import cryptography
from datetime import datetime
from collections import OrderedDict


from blockone.base import BlockOneBase
from blockone.block import Block
from blockone.transaction import BlockOneTransaction
import blockone.constants as ct



class BlockOneChain(BlockOneBase):
  def __init__(self, initial_difficulty=3, **kwargs):
    super(BlockOneChain, self).__init__(**kwargs)
    self.chain = []
    self.difficulty = initial_difficulty
    self.reset_transactions()
    self.name = self.__class__.__name__
    self.P("Initializing on cryptography v.{}".format(cryptography.__version__))
    return
  
  @classmethod
  def from_message(cls, str_json, log):
    obj = cls(log=log)
    dct_data = json.loads(str_json)
    for k in dct_data:
      vars(obj)[k] = dct_data[k]
    return obj
  
  
  def update_chain(self, str_json):
    dct_data = json.loads(str_json)
    for k in dct_data:
      vars(self)[k] = dct_data[k]
    return
        
    
  
  def maybe_increment_difficulty(self):
    self.difficulty += 1
    return
  
  
  def get_timestamp(self):
    return datetime.now().strftime('%Y%m%d%H%M%S%f') 
  
  
  def get_unconfirmed(self, filter_address=None, data_subkey=None, data_value=None):
    res = [x for x in self.unconfirmed_transactions]
    if filter_address is not None:
      res = [x for x in res if x[ct.TRAN.SND] == filter_address]
    if data_subkey is not None:
      res = [x for x in res if x[ct.TRAN.DATA][data_subkey] == data_value]
    return [x for x in res]
    
  
  def create_genesys_block(self, client_zero):
    tx = BlockOneTransaction(
      snd='Genesis',
      data=dict(
        rcv=client_zero,
        val=500,
        )
      )
    gen_blk = Block(
      index=0,
      block_name='Genesis',
      transactions=[tx.to_dict()],
      timestamp=self.get_timestamp(),
      previous_hash="0",
      )
    gen_blk.block_hash = gen_blk.compute_hash()
    self._add_block(gen_blk)
    return
  
  
  def add_new_transaction(self, transaction: BlockOneTransaction):
    check_ok, msg = self.verify_transaction(
        tx=transaction, 
       )
    if not check_ok:
      self.P("Transaction failed: {}".format(msg))
      return
      
    dct_trans = transaction.to_dict()
    dct_trans[ct.TRAN.TXSIGN] = transaction.tx_sign
    self.unconfirmed_transactions.append(dct_trans)
    self.P("Transaction added succesfully to pending transactions. Signature: {}/{}".format(check_ok, msg))
    return
    
  def reset_transactions(self):
    self.unconfirmed_transactions = []
  
  
  @property
  def last_block(self):
    return self.chain[-1]
  
  @property
  def chain_size(self):
    return len(self.chain)

  
  def is_difficulty_valid(self, block: Block, proof: str):
    required_start = '0' * self.difficulty
    is_start_valid = proof.startswith(required_start)
    return is_start_valid
  
  
  def is_proof_of_work_valid(self, block: Block, proof: str):
    is_hash_valid = proof == block.compute_hash()
    is_diff_valid = self.is_difficulty_valid(block=block, proof=proof)
    return is_diff_valid and is_hash_valid
  
  def _add_block(self, block: Block):
    self.chain.append(block.to_dict())
  
  def add_block(self, block : Block, proof, miner):
    previous_hash = self.last_block['block_hash']
    if previous_hash != block.previous_hash:
      self.P("Block creation failed. Last block hash differs from proposed block last-hash")
      return False
    
    if not self.is_proof_of_work_valid(block=block, proof=proof):
      return False
    else:
      self.P("PoW valid from miner {}".format(miner))
    
    block.block_hash = proof
    block.miner = miner
    self._add_block(block)
    self.maybe_increment_difficulty()
    return True

  
  def dump_blockchain(self):
    barsize = 110
    sz = self.chain_size
    self.P("=" * barsize)
    self.P("Dumping full blockchain with {} blocks".format(sz))
    for bidx in range(sz):
      blk = self.chain[bidx]
      self.P("  Block #{} '{}':".format(blk['index'],blk['block_name']))
      trans = blk['transactions']
      for tx in trans:
        snd = tx[ct.TRAN.SND]
        data = tx[ct.TRAN.DATA]
        self.P("    FROM: {}  DATA: {}".format(snd, data))
    self.P("-" * barsize)
    self.P("  Unconfirmed transactions:")
    utxs = self.get_unconfirmed()
    for uidx in range(len(utxs)):
      utx = utxs[uidx]
      snd = utx[ct.TRAN.SND]
      data = utx[ct.TRAN.DATA]
      self.P("    ** FROM: {}  DATA: {}".format(snd, data))
      
    return
  
  def verify_transaction(self, tx):
    # first we extract needed info from transaction
    if isinstance(tx, BlockOneTransaction):
      tx_sign = tx.tx_sign
      tx_snd = tx.snd
      tx_snd_pk = tx_snd
      tx_dump = tx.to_message()
      tx_method = tx._method
    elif isinstance(tx, dict):
      tx_sign = tx[ct.TRAN.TXSIGN]
      tx_snd = tx[ct.TRAN.SND]
      tx_snd_pk = tx_snd
      dct_new = {k:v for k,v in tx.items() if k not in ct.TRAN.EXTERNAL}
      tx_dump = self._to_message(dct_new)
      tx_method = tx[ct.TRAN.METHOD]

    # OBSOLETE: we compare the sender address with the public key  
    ### Obs: we use directly usable addresses
    # addr1 = ct.ENC.ADDRESS_PREFIX + tx_snd_pk
    
    # if  addr1 != tx_snd:
    #   return False, "Verification failed. Forged address/key: SND: '{}' vs SND_PK: '{}'".format(
    #     tx_snd, addr1)
    
    # now we verify the signature
    tx_snd_pk = tx_snd_pk[len(ct.ENC.ADDRESS_PREFIX):]
    res = self.verify(
      data=tx_dump,
      signature=tx_sign,
      public_key=tx_snd_pk,
      method=tx_method,
      )    
    return res
  
  
  def check_local_integrity(self):
    self.P("Checking local blockchain integrity...")
    for blk in self.chain:
      dct_test_block = OrderedDict({k:v for k,v in blk.items() 
                                    if k not in ct.BLOCK.EXTERNAL})
      h = self._compute_hash(dct_test_block)
      if h != blk[ct.BLOCK.HASH]:
        self.P("  ERROR: Integrity check failed at block #{}. Block hash has been tampered!".format(
          blk[ct.BLOCK.INDEX]))
        return False
      trans = blk[ct.BLOCK.TRANS]
      for tran in trans:
        dct_test_tran = OrderedDict({k:v for k,v in tran.items() 
                                     if k not in ct.TRAN.EXTERNAL})
        txh = self._compute_hash(dct_test_tran)
        txh_orig = tran[ct.TRAN.TXHASH]
        if  txh_orig != txh:
          self.P("  ERROR: Integrity check failed at block #{} - Tran #{}. Block hash has been tampered!".format(
            blk[ct.BLOCK.INDEX], txh_orig))
          return False
    self.P("Done checking. All clear.")
    return True


  def __repr__(self):
    res = '{}\n'.format(self.__class__.__name__)
    res = res  + self.to_message()
    return res

  
  def to_message(self):
    dct_out = {
       ct.CHAIN : self.chain,
       ct.ENC.DIFFICULTY : self.difficulty,
       ct.UNCONF : self.unconfirmed_transactions,
      }
    str_chain = self._to_message(dct_out)
    return str_chain
  
