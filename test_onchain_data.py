
from blockone.transaction import BlockOneTransaction
from blockone.chain import BlockOneChain
from blockone.miner import BlockOneMiner
from blockone.client import BlockOneClient

from blockone.logger import Logger
  
if __name__ == '__main__':
  
  log = Logger("BO", base_folder='.', app_folder='_cache')
  
  ###
  ###
  ### On-chain data test
  ###
  ###
  
  chain = BlockOneChain(log=log)

  client1 = BlockOneClient(
    blockchain=chain, 
    name='Client A', 
    family_name='', 
    log=log
    )
  chain.create_genesys_block(client1.address)
  

  miner = BlockOneMiner(chain, log=log)
  
  client2 = BlockOneClient(
    blockchain=chain, 
    name='Client B', 
    family_name='', 
    log=log
    )
  
  log.P("* adding good tran")
  tx1 = BlockOneTransaction(    
    snd=client1.address,
    data=dict(
      rcv=client2.address,
      val=1,
      message='This is a message...',
      data11=b'1234566000000000000000000000000000000000000',
      data12=b'1234566000000000000000000000000000000000000'
      )
    )
  sign1 = client1.sign_transaction(tx1)
  # TODO: next instruction is incomplete. "chain" must in fact send the tx to a miner
  # that will check the transaction and propagate - later a block will be mined
  # so the miner needs to verify both the signature as well any conditions such as
  # the availability of amount to be spend
  # also the miner should be "paid" (at least registered as such) in the "coinbase" tx
  # of each new block
  chain.add_new_transaction(tx1) 

  
  log.P("* adding good tran")
  tx2 = BlockOneTransaction(
    snd=client1.address,
    data=dict(
      rcv=client2.address,
      val=1,
      message='This is another message...',
      bin21=b'23132732327777722',
      msg22=b'1231312312aaaaaaaaaaadASDSSSSSSSSSSSSSSSS'
      )
    )
  sign2 = client1.sign_transaction(tx2)
  chain.add_new_transaction(tx2)
  
  log.P(client1)
  log.P(client2)
  miner.mine()
  log.P(client1)
  log.P(client2)
  
  log.P("* adding bad tran")
  tx3 = BlockOneTransaction(
    snd=client1.address,
    data=dict(
      rcv=client2.address,
      val=1,
      message='This is yet another message...'
      ),
    name='bad'
    )  
  # now we forge the validation
  tx3._sender_public_key = tx2._sender_public_key # use another pk
  tx3.tx_sign = tx2.tx_sign # use another previosly generated signature
  tx3._method = tx2._method 
  # now we ask the chain to add the transaction for the miners to mine
  chain.add_new_transaction(tx3)

  log.P(client1)
  log.P(client2)
  miner.mine()
  log.P(client1)
  log.P(client2)

  log.P("* adding good tran")
  tx4 = BlockOneTransaction(
    snd=client1.address,
    data=dict(
      rcv=client2.address,
      val=1,
      message='This is ... well ... another message...'
      )
    )  
  sign4 = client1.sign_transaction(tx4)
  chain.add_new_transaction(tx4)

  log.P(client1)
  log.P(client2)
  
  chain.dump_blockchain()
  log.P(chain)
  saved = chain.to_message()

  # now we move to another miner
  remote_chain = BlockOneChain.from_message(
    str_json=saved,
    log=log
    ) 
  remote_miner = BlockOneMiner(
    remote_chain, 
    name='MinerRemote1',
    log=log
    )
  remote_miner.mine()

  log.P(remote_chain)  
  remote_chain.check_local_integrity()
  remote_save = remote_chain.to_message()

  # the remote synchronizes with the network
  # data is received locally
  chain.update_chain(remote_save)
  # now clients connect to check their jobs / statuses / wallets / etc
  log.P(client1)
  log.P(client2)
  
