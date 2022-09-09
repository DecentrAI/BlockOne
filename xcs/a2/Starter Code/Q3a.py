from sys import exit
from bitcoin.core.script import *
from bitcoin.wallet import CBitcoinSecret

from lib.utils import *
from lib.config import (my_private_key, my_public_key, my_address,
                    faucet_address, network_type)
from Q1 import send_from_P2PKH_transaction


cust1_private_key = CBitcoinSecret(
    'cVjuUuz4aHE3wEeDK24jR4mHqXLog5oQBPJjA3SKHSora7YEApGq') # mp5Vixg38Y7aZPDfwP1NsJGxeqiYV7KiJi
cust1_public_key = cust1_private_key.pub
cust2_private_key = CBitcoinSecret(
    'cR6PB8oSSeabh1yC768THhaqC6qxQE1Fa9rvbSBTtzWU6Lotjc3v') # mk7zft7cqRHLz2u1phS4cv1CarayWi64Mq
cust2_public_key = cust2_private_key.pub
cust3_private_key = CBitcoinSecret(
    'cTiwqsMBbCsnL6gZy5xj2NkbyuEk3JzVfYLgX4tERxJgNa5Rcy1B') # n2Gnb2UkphZZUCJ8asLdpNAVN9pHbhk6FB
cust3_public_key = cust3_private_key.pub


######################################################################
# TODO: Complete the scriptPubKey implementation for Exercise 3

# You can assume the role of the bank for the purposes of this problem
# and use my_public_key and my_private_key in lieu of bank_public_key and
# bank_private_key.

Q3a_txout_scriptPubKey = [
        # fill this in!
        ## op_0
        ## any_sig
        ## my_sig
        my_public_key,
        OP_CHECKSIG,
        OP_1,
        cust1_public_key,
        cust2_public_key,
        cust3_public_key,
        OP_3,
        OP_CHECKMULTISIG,  
]
######################################################################

if __name__ == '__main__':
    ######################################################################
    # TODO: set these parameters correctly
    amount_to_send = 0.002 # amount of BTC in the output you're sending minus fee
    txid_to_spend = (
        '25d8399b921addf5ad4ce54a3cc130815fc34ecd0284642a045f03d67fe90f63')
    utxo_index = 0 # index of the output you are spending, indices start at 0
    ######################################################################

    response = send_from_P2PKH_transaction(amount_to_send, txid_to_spend, 
        utxo_index, Q3a_txout_scriptPubKey, my_private_key, network_type)
    print(response.status_code, response.reason)
    print(response.text)




# Current network type: btc-test3 INITIAL
# 201 Created
# {
#   "tx": {
#     "block_height": -1,
#     "block_index": -1,
#     "hash": "cd7caa2274a333e68440feb54dc409d1c44bcc0989c0152e5f405aad68ab4e1a",
#     "addresses": [
#       "mo5cT5Qc7t4LyH5impMnx8g54wrhjkMzXD",
#       "zWobro7ynRYfwXTTtvbzHovdQxBHZoVP3i"
#     ],
#     "total": 100000,
#     "fees": 233333,
#     "size": 306,
#     "vsize": 306,
#     "preference": "high",
#     "relayed_by": "2a02:2f0e:e02:b300:d908:df3b:f405:3b90",
#     "received": "2022-09-09T07:46:45.164080948Z",
#     "ver": 1,
#     "double_spend": false,
#     "vin_sz": 1,
#     "vout_sz": 1,
#     "confirmations": 0,
#     "inputs": [
#       {
#         "prev_hash": "de868de88ab6c0779b316fce9d9855abd5f9ddf0d1cfaf1f046c7cbccc61bec2",
#         "output_index": 8,
#         "script": "4730440220134163ec300de04e67969786794dcd557895a78c9fd9f17bff8a3e69d5fea3a102202576440a0dfb8f4856c3b844a5209f6a11882942c8100f662819173be66e51400121029ee00a3fc4962cdfda3bdd1daf6d837247ee973c3476e7636d6beec2b4f0a96f",
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
#         "script": "21029ee00a3fc4962cdfda3bdd1daf6d837247ee973c3476e7636d6beec2b4f0a96fac5121031881a520198d5792ba0b04b86304fa449a424aefaa9daed37cf0c5c61737dcb42103b023fb82b3e9cd3c7246f8698aac7a57f8f8176f0076f03143ce432854a5686121027ac8d398d4f7e448af139c2291aeb11a3bbb5ca4cc5b43503241027e146d5e3f53ae",
#         "addresses": [
#           "zWobro7ynRYfwXTTtvbzHovdQxBHZoVP3i"
#         ],
#         "script_type": "pay-to-multi-pubkey-hash"
#       }
#     ]
#   }
# }