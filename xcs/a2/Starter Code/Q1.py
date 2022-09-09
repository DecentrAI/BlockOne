from bitcoin.core.script import *
from bitcoin.wallet import CBitcoinSecret, P2PKHBitcoinAddress

from lib.utils import *
from lib.config import (my_private_key, my_public_key, my_address,
                    faucet_address, network_type)


def P2PKH_scriptPubKey(address):
    ######################################################################
    # TODO: Complete the standard scriptPubKey implementation for a
    # PayToPublicKeyHash transaction
    return [
        # fill this in! OP_DUP OP_HASH160 address OP_EQUALVERIFY OP_CHECKSIG
        OP_DUP,
        OP_HASH160,
        address,
        OP_EQUALVERIFY,
        OP_CHECKSIG,
    ]
    ######################################################################


def P2PKH_scriptSig(txin, txout, txin_scriptPubKey, private_key, public_key):
    signature = create_OP_CHECKSIG_signature(txin, txout, txin_scriptPubKey,
                                             private_key)
    ######################################################################
    # TODO: Complete this script to unlock the BTC that was sent to you
    # in the PayToPublicKeyHash transaction.
    return [
        # fill this in! signature public_key
        signature,
        public_key
        
    ]
    ######################################################################

def send_from_P2PKH_transaction(amount_to_send,
                                txid_to_spend,
                                utxo_index,
                                txout_scriptPubKey,
                                sender_private_key,
                                network):

    sender_public_key = sender_private_key.pub
    sender_address = P2PKHBitcoinAddress.from_pubkey(sender_public_key)

    txout = create_txout(amount_to_send, txout_scriptPubKey)

    txin_scriptPubKey = P2PKH_scriptPubKey(sender_address)
    txin = create_txin(txid_to_spend, utxo_index)
    txin_scriptSig = P2PKH_scriptSig(txin, txout, txin_scriptPubKey,
        sender_private_key, sender_public_key)

    new_tx = create_signed_transaction(txin, txout, txin_scriptPubKey,
                                       txin_scriptSig)

    return broadcast_transaction(new_tx, network)


if __name__ == '__main__':
    ######################################################################
    # TODO: set these parameters correctly
    amount_to_send = 0.001 # amount of BTC in the output you're sending minus fee
    txid_to_spend = (
        'de868de88ab6c0779b316fce9d9855abd5f9ddf0d1cfaf1f046c7cbccc61bec2')
    utxo_index = 6 # index of the output you are spending, indices start at 0
    ######################################################################

    txout_scriptPubKey = P2PKH_scriptPubKey(faucet_address)
    response = send_from_P2PKH_transaction(
        amount_to_send,
        txid_to_spend,
        utxo_index,
        txout_scriptPubKey,
        my_private_key,
        network_type,
    )
    print(response.status_code, response.reason)
    print(response.text)



# Current network type: btc-test3 - THIRD !!!
# 201 Created
# {
#   "tx": {
#     "block_height": -1,
#     "block_index": -1,
#     "hash": "25d2f5a8a9c3a7ea2f07e0df77ca4cea46979efd835ef100d3f8e52a02d0787e",
#     "addresses": [
#       "mo5cT5Qc7t4LyH5impMnx8g54wrhjkMzXD",
#       "mv4rnyY3Su5gjcDNzbMLKBQkBicCtHUtFB"
#     ],
#     "total": 100000,
#     "fees": 233333,
#     "size": 191,
#     "vsize": 191,
#     "preference": "high",
#     "relayed_by": "2a02:2f0e:e02:b300:d908:df3b:f405:3b90",
#     "received": "2022-09-09T17:38:00.985242219Z",
#     "ver": 1,
#     "double_spend": false,
#     "vin_sz": 1,
#     "vout_sz": 1,
#     "confirmations": 0,
#     "inputs": [
#       {
#         "prev_hash": "de868de88ab6c0779b316fce9d9855abd5f9ddf0d1cfaf1f046c7cbccc61bec2",
#         "output_index": 6,
#         "script": "4730440220516c1b2be973e958b66ae88ce9042fccc1fae6b8f73fdefb2d45c31a79d67947022053dd9fe574ccddedf7fb9ba5dfd8b5d3cf455999527db5452ee72df73bae3d700121029ee00a3fc4962cdfda3bdd1daf6d837247ee973c3476e7636d6beec2b4f0a96f",
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
#         "script": "76a9149f9a7abd600c0caa03983a77c8c3df8e062cb2fa88ac",
#         "addresses": [
#           "mv4rnyY3Su5gjcDNzbMLKBQkBicCtHUtFB"
#         ],
#         "script_type": "pay-to-pubkey-hash"
#       }
#     ]
#   }
# }

# Current network type: btc-test3 -- SECOND
# 201 Created
# {
#   "tx": {
#     "block_height": -1,
#     "block_index": -1,
#     "hash": "b39a77b884e5d02bca37ecb85a179d4bc07304acd53564b6005bbc2de7c8e702",
#     "addresses": [
#       "mv4rnyY3Su5gjcDNzbMLKBQkBicCtHUtFB",
#       "mo5cT5Qc7t4LyH5impMnx8g54wrhjkMzXD"
#     ],
#     "total": 100000,
#     "fees": 233333,
#     "size": 192,
#     "vsize": 192,
#     "preference": "high",
#     "relayed_by": "2a02:2f0e:e02:b300:d908:df3b:f405:3b90",
#     "received": "2022-09-09T05:35:17.468229171Z",
#     "ver": 1,
#     "double_spend": false,
#     "vin_sz": 1,
#     "vout_sz": 1,
#     "confirmations": 0,
#     "inputs": [
#       {
#         "prev_hash": "de868de88ab6c0779b316fce9d9855abd5f9ddf0d1cfaf1f046c7cbccc61bec2",
#         "output_index": 6,
#         "script": "483045022100a0b6bcc6ef84b2b49aa49b7c34ae5652b4040a40265e04dff3219dd0ef7d4fc902204e7054fa5d3d1b051ac0cfb99f093412a8c43ed73d98cfff98dd9369bf65c5010121029ee00a3fc4962cdfda3bdd1daf6d837247ee973c3476e7636d6beec2b4f0a96f",
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
#         "script": "76a9149f9a7abd600c0caa03983a77c8c3df8e062cb2fa88ac",
#         "addresses": [
#           "mv4rnyY3Su5gjcDNzbMLKBQkBicCtHUtFB"
#         ],
#         "script_type": "pay-to-pubkey-hash"
#       }
#     ]
#   }
# }

# Current network type: btc-test3 -- INITIAL
# 201 Created
# {
#   "tx": {
#     "block_height": -1,
#     "block_index": -1,
#     "hash": "2c9ef022737c4a46ec39679bd3a43b0ed53ae037a94237bcb0e0452385ed865c",
#     "addresses": [
#       "mv4rnyY3Su5gjcDNzbMLKBQkBicCtHUtFB",
#       "mo5cT5Qc7t4LyH5impMnx8g54wrhjkMzXD"
#     ],
#     "total": 200000,
#     "fees": 133333,
#     "size": 191,
#     "vsize": 191,
#     "preference": "high",
#     "relayed_by": "2a02:2f0e:e02:b300:c47:3f75:7fb2:4a5d",
#     "received": "2022-09-08T11:51:58.732429744Z",
#     "ver": 1,
#     "double_spend": false,
#     "vin_sz": 1,
#     "vout_sz": 1,
#     "confirmations": 0,
#     "inputs": [
#       {
#         "prev_hash": "de868de88ab6c0779b316fce9d9855abd5f9ddf0d1cfaf1f046c7cbccc61bec2",
#         "output_index": 0,
#         "script": "473044022033d06e142b5228ba0656c9d903d167340accd761e4be93cf650c356b084dacad02207d18f8ef82678385e0c1dc460dbb28bc596a292f147513aa305fb904a27608b20121029ee00a3fc4962cdfda3bdd1daf6d837247ee973c3476e7636d6beec2b4f0a96f",
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
#         "value": 200000,
#         "script": "76a9149f9a7abd600c0caa03983a77c8c3df8e062cb2fa88ac",
#         "addresses": [
#           "mv4rnyY3Su5gjcDNzbMLKBQkBicCtHUtFB"
#         ],
#         "script_type": "pay-to-pubkey-hash"
#       }
#     ]
#   }
# }