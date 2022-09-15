from sys import exit
from bitcoin.core.script import *

from lib.utils import *
from lib.config import (my_private_key, my_public_key, my_address,
                    faucet_address, network_type)
from Q1 import P2PKH_scriptPubKey
from Q3a import (Q3a_txout_scriptPubKey, cust1_private_key, cust2_private_key,
                  cust3_private_key)


def multisig_scriptSig(txin, txout, txin_scriptPubKey):
    bank_sig = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey,
                                             my_private_key)
    cust1_sig = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey,
                                             cust1_private_key)
    cust2_sig = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey,
                                             cust2_private_key)
    cust3_sig = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey,
                                             cust3_private_key)
    ######################################################################
    # TODO: Complete this script to unlock the BTC that was locked in the
    # multisig transaction created in Exercise 3a.
    return [
        # fill this in!
        OP_0,
        cust1_sig,
        bank_sig,        
    ]
    ######################################################################


def send_from_multisig_transaction(amount_to_send, txid_to_spend, utxo_index,
                                   txin_scriptPubKey, txout_scriptPubKey, network):
    txout = create_txout(amount_to_send, txout_scriptPubKey)

    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = multisig_scriptSig(txin, txout, txin_scriptPubKey)

    new_tx = create_signed_transaction(txin, txout, txin_scriptPubKey,
                                       txin_scriptSig)

    return broadcast_transaction(new_tx, network)

if __name__ == '__main__':
    ######################################################################
    # TODO: set these parameters correctly
    amount_to_send = 0.001 # amount of BTC in the output you're sending minus fee
    txid_to_spend = (
        '9549f1ca2ea0a28cf4d6c746e34b1320385ae3209c6e9dc5b7aa47f62f3be3cd')
    utxo_index = 0 # index of the output you are spending, indices start at 0
    ######################################################################

    txin_scriptPubKey = Q3a_txout_scriptPubKey
    txout_scriptPubKey = P2PKH_scriptPubKey(faucet_address)

    response = send_from_multisig_transaction(
        amount_to_send, txid_to_spend, utxo_index,
        txin_scriptPubKey, txout_scriptPubKey, network_type)
    print(response.status_code, response.reason)
    print(response.text)
    
    
# Current network type: btc-test3
# 201 Created
# {
#   "tx": {
#     "block_height": -1,
#     "block_index": -1,
#     "hash": "50289a24879f305e60fadad290fce4ed9157b8da3ba7a3aa4dae937bc3da7f1e",
#     "addresses": [
#       "zXtktnDu9KgVypFh7cT1qpYxomWoJjz8my",
#       "mv4rnyY3Su5gjcDNzbMLKBQkBicCtHUtFB"
#     ],
#     "total": 100000,
#     "fees": 100000,
#     "size": 230,
#     "vsize": 230,
#     "preference": "high",
#     "relayed_by": "92.85.42.116",
#     "received": "2022-09-12T08:46:58.104712919Z",
#     "ver": 1,
#     "double_spend": false,
#     "vin_sz": 1,
#     "vout_sz": 1,
#     "confirmations": 0,
#     "inputs": [
#       {
#         "prev_hash": "9549f1ca2ea0a28cf4d6c746e34b1320385ae3209c6e9dc5b7aa47f62f3be3cd",
#         "output_index": 0,
#         "script": "0047304402205f54ceb4fe11f0423ed8c2dcf8aa24d9854baa87b5b531b612417386e9b7ad5c02204a76480ebe61ad416009feb302114e2dc1ce37be7ad67ecb557befa9eff6be3b0147304402205ceec641100239c76dedad17e77efea7bbb1b977d5619d3958b9d7da9a9f056f02207db366291ab61b237753d81408f3f1975e1914cb262ed8586a83279205def3df01",
#         "output_value": 200000,
#         "sequence": 4294967295,
#         "addresses": [
#           "zXtktnDu9KgVypFh7cT1qpYxomWoJjz8my"
#         ],
#         "script_type": "pay-to-multi-pubkey-hash",
#         "age": 2346264
#       }
#     ],
#     "outputs": [
#       {
#         "value": 100000,
#         "script": "76a9149f9a7abd600c0caa03983a77c8c3df8e062cb2fa88ac",
#         "addresses": [
#           "mv4rnyY3Su5gjcDNzbMLKBQkBicCtHUtFB"
#         ],
#         "script_type": "pay-to-pubkey-hash"
#       }
#     ]
#   }
# }
