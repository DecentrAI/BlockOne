from sys import exit
from bitcoin.core.script import *
from bitcoin.core import x

from lib.utils import *
from lib.config import (my_private_key, my_public_key, my_address,
                    faucet_address, network_type)
from Q1 import send_from_P2PKH_transaction

from bitcoin.core.serialize import VarIntSerializer

######################################################################
# TODO: Complete the scriptPubKey implementation for Exercise 2
Q2a_txout_scriptPubKey = [
  OP_2DUP,
  OP_ADD,
  OP_HASH160,
  x('77b02e695de599bbbd1549a9277ac4ed141e986f'), 
  OP_EQUALVERIFY,
  OP_SUB,
  Hash160()
  OP_HASH160,
  x('9e25324a2452227c7ba636470d2c36e72c12b675'), 
  OP_EQUAL,
 ]
######################################################################

if __name__ == '__main__':
  # from bitcoin.core.serialize import VarIntSerializer
  # v = VarIntSerializer.serialize(1976)

  ######################################################################
  # TODO: set these parameters correctly
  amount_to_send = 0.0015 # amount of BTC in the output you're sending minus fee
  txid_to_spend = (
      'de868de88ab6c0779b316fce9d9855abd5f9ddf0d1cfaf1f046c7cbccc61bec2')
  utxo_index = 5 # index of the output you are spending, indices start at 0
  ######################################################################

  response = send_from_P2PKH_transaction(
      amount_to_send, txid_to_spend, utxo_index,
      Q2a_txout_scriptPubKey, my_private_key, network_type)
  print(response.status_code, response.reason)
  print(response.text)


# Current network type: btc-test3
# 201 Created
# {
#   "tx": {
#     "block_height": -1,
#     "block_index": -1,
#     "hash": "aee7801c6dfadf0b5093f0ebc75d7a63ff74b74a321c76d523c0b3e59ed13502",
#     "addresses": [
#       "mo5cT5Qc7t4LyH5impMnx8g54wrhjkMzXD"
#     ],
#     "total": 100000,
#     "fees": 233333,
#     "size": 216,
#     "vsize": 216,
#     "preference": "high",
#     "relayed_by": "2a02:2f0e:e02:b300:c47:3f75:7fb2:4a5d",
#     "received": "2022-09-08T21:10:38.192792794Z",
#     "ver": 1,
#     "double_spend": false,
#     "vin_sz": 1,
#     "vout_sz": 1,
#     "confirmations": 0,
#     "inputs": [
#       {
#         "prev_hash": "de868de88ab6c0779b316fce9d9855abd5f9ddf0d1cfaf1f046c7cbccc61bec2",
#         "output_index": 5,
#         "script": "483045022100b0b95f143ba090f5d283ccdb1adc36cb5b75f55baf8917e8a10e3bdc527660c50220494e60a5d0211c752740dcc8cc45e0d0b7369d3ee4c09ad1629af103950c770a0121029ee00a3fc4962cdfda3bdd1daf6d837247ee973c3476e7636d6beec2b4f0a96f",
#         "output_value": 333333,
#         "sequence": 4294967295,
#         "addresses": [
#           "mo5cT5Qc7t4LyH5impMnx8g54wrhjkMzXD"
#         ],
#         "script_type": "pay-to-pubkey-hash",
#         "age": 2345495
#       }
#     ],
#     "outputs": [
#       {
#         "value": 100000,
#         "script": "6e93a91477b02e695de599bbbd1549a9277ac4ed141e986f8894a9149e25324a2452227c7ba636470d2c36e72c12b67587",
#         "addresses": null,
#         "script_type": "unknown"
#       }
#     ]
#   }
# }