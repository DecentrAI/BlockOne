from sys import exit
from bitcoin.core.script import *

from lib.utils import *
from lib.config import (my_private_key, my_public_key, my_address,
                    faucet_address, network_type)
from Q1 import P2PKH_scriptPubKey
from Q2a import Q2a_txout_scriptPubKey


######################################################################
# TODO: set these parameters correctly
amount_to_send = 0.0001 # amount of BTC in the output you're sending minus fee 
txid_to_spend = (
        'aee7801c6dfadf0b5093f0ebc75d7a63ff74b74a321c76d523c0b3e59ed13502')
utxo_index = 0 # index of the output you are spending, indices start at 0
######################################################################

txin_scriptPubKey = Q2a_txout_scriptPubKey
######################################################################
# TODO: implement the scriptSig for redeeming the transaction created
# in  Exercise 2a.
txin_scriptSig = [
        1051,
        925
]
######################################################################
txout_scriptPubKey = P2PKH_scriptPubKey(faucet_address)

response = send_from_custom_transaction(
    amount_to_send, txid_to_spend, utxo_index,
    txin_scriptPubKey, txin_scriptSig, txout_scriptPubKey, network_type)
print(response.status_code, response.reason)
print(response.text)



# Current network type: btc-test3 SECOND
# 201 Created
# {
#   "tx": {
#     "block_height": -1,
#     "block_index": -1,
#     "hash": "47b1f24106a3e3c5b9cb86a0c9fb724096c6a2f8458472d98b513cd457da9e01",
#     "addresses": [
#       "mv4rnyY3Su5gjcDNzbMLKBQkBicCtHUtFB"
#     ],
#     "total": 10000,
#     "fees": 90000,
#     "size": 91,
#     "vsize": 91,
#     "preference": "high",
#     "relayed_by": "2a02:2f0e:e02:b300:d908:df3b:f405:3b90",
#     "received": "2022-09-09T17:43:43.545002391Z",
#     "ver": 1,
#     "double_spend": false,
#     "vin_sz": 1,
#     "vout_sz": 1,
#     "confirmations": 0,
#     "inputs": [
#       {
#         "prev_hash": "aee7801c6dfadf0b5093f0ebc75d7a63ff74b74a321c76d523c0b3e59ed13502",
#         "output_index": 0,
#         "script": "021b04029d03",
#         "output_value": 100000,
#         "sequence": 4294967295,
#         "script_type": "unknown",
#         "age": 2345870
#       }
#     ],
#     "outputs": [
#       {
#         "value": 10000,
#         "script": "76a9149f9a7abd600c0caa03983a77c8c3df8e062cb2fa88ac",
#         "addresses": [
#           "mv4rnyY3Su5gjcDNzbMLKBQkBicCtHUtFB"
#         ],
#         "script_type": "pay-to-pubkey-hash"
#       }
#     ]
#   }
# }



# INITIAL:
# Current network type: btc-test3
# 201 Created
# {
#   "tx": {
#     "block_height": -1,
#     "block_index": -1,
#     "hash": "f979ac0703f948b0ccaf72d4b17916c848e1bc24850359935f7971b82c48f4d0",
#     "addresses": [
#       "mv4rnyY3Su5gjcDNzbMLKBQkBicCtHUtFB"
#     ],
#     "total": 80000,
#     "fees": 20000,
#     "size": 91,
#     "vsize": 91,
#     "preference": "high",
#     "relayed_by": "2a02:2f0e:e02:b300:d908:df3b:f405:3b90",
#     "received": "2022-09-09T05:05:42.166565754Z",
#     "ver": 1,
#     "double_spend": false,
#     "vin_sz": 1,
#     "vout_sz": 1,
#     "confirmations": 0,
#     "inputs": [
#       {
#         "prev_hash": "aee7801c6dfadf0b5093f0ebc75d7a63ff74b74a321c76d523c0b3e59ed13502",
#         "output_index": 0,
#         "script": "021b04029d03",
#         "output_value": 100000,
#         "sequence": 4294967295,
#         "script_type": "unknown",
#         "age": 0
#       }
#     ],
#     "outputs": [
#       {
#         "value": 80000,
#         "script": "76a9149f9a7abd600c0caa03983a77c8c3df8e062cb2fa88ac",
#         "addresses": [
#           "mv4rnyY3Su5gjcDNzbMLKBQkBicCtHUtFB"
#         ],
#         "script_type": "pay-to-pubkey-hash"
#       }
#     ]
#   }
# }