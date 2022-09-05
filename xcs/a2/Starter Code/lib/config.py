from bitcoin import SelectParams
from bitcoin.base58 import decode
from bitcoin.core import x
from bitcoin.wallet import CBitcoinAddress, CBitcoinSecret, P2PKHBitcoinAddress


SelectParams('testnet')

faucet_address = CBitcoinAddress('mv4rnyY3Su5gjcDNzbMLKBQkBicCtHUtFB')

# For questions 1-3, we are using 'btc-test3' network. For question 4, you will
# set this to be either 'btc-test3' or 'bcy-test'
network_type = 'bcy-test'


######################################################################
# This section is for Questions 1-3
# TODO: Fill this in with your private key.
#
# Create a private key and address pair in Base58 with keygen.py
# Send coins at https://testnet-faucet.mempool.co/

my_private_key = CBitcoinSecret(
    'cTzJVdfR3syC98Ycsfrx98aUJ1X5Wh5jHwHjjzrrXaKpL2yXT7cp') 
# mo5cT5Qc7t4LyH5impMnx8g54wrhjkMzXD
# txin = a932b79ade5eda54c1c329812f9ffc1c73cc0b2c665b5e89124e386a108cecc7
# split 9x tran: de868de88ab6c0779b316fce9d9855abd5f9ddf0d1cfaf1f046c7cbccc61bec2

my_public_key = my_private_key.pub
my_address = P2PKHBitcoinAddress.from_pubkey(my_public_key)
######################################################################


######################################################################
# NOTE: This section is for Question 4
# TODO: Fill this in with address secret key for BTC testnet3
#
# Create address in Base58 with keygen.py
# Send coins at https://testnet-faucet.mempool.co/

# Only to be imported by alice.py
# Alice should have coins!!
alice_secret_key_BTC = CBitcoinSecret(
    'cMhKQWStEaZm7UMJAaHt9aQQ5zBmZ2Ga9m2er1ztZKTcM7bYUUyr')
# my22CZ1vY9sywotrpVwaSE4Q8UX3U7cgzy
# txin: 3d72f2f802c2eee5d025ed03ae257ba49805f066268fa56a5fee5b3a910b4646
# split 9x tran: 2786afbdc7bc13f9ee5db84e97e2bde1aba37df3e32b94202a8e77919d785136

# Only to be imported by bob.py
bob_secret_key_BTC = CBitcoinSecret(
    'cUxKQxpNj3qtXXuvN6uE4s2M8sN8UavDidn4DgCN63U2s3Pjfqvi')
# n2BX8rnsVqcAjteNqjCDg3LWvudr6XokWf

# Can be imported by alice.py or bob.py
alice_public_key_BTC = alice_secret_key_BTC.pub
alice_address_BTC = P2PKHBitcoinAddress.from_pubkey(alice_public_key_BTC)

bob_public_key_BTC = bob_secret_key_BTC.pub
bob_address_BTC = P2PKHBitcoinAddress.from_pubkey(bob_public_key_BTC)
######################################################################


######################################################################
# NOTE: This section is for Question 4
# TODO: Fill this in with address secret key for BCY testnet
#
# Create address in hex with
# curl -X POST "https://api.blockcypher.com/v1/bcy/test/addrs?token=c2de833f616f4ac48a6b90cbcb2c6b40"
# This request will return a private key, public key and address. Make sure to save these.
#
# Send coins with
# curl -d '{"address": "CCbDfAdViTrL3ecSmpqFtTr3pW2AUCuEKf", "amount": 1000000}' 'https://api.blockcypher.com/v1/bcy/test/faucet?token=c2de833f616f4ac48a6b90cbcb2c6b40'
# This request will return a transaction reference. Make sure to save this.

# Only to be imported by alice.py
alice_secret_key_BCY = CBitcoinSecret.from_secret_bytes(
    x('52315abf87035ac3ae4cb57e6d874f962dcfa3560cb96ecc4e4d0830380c66e1'))
# {
#   "private": "52315abf87035ac3ae4cb57e6d874f962dcfa3560cb96ecc4e4d0830380c66e1",
#   "public": "033b253c2cbca29f4b728521a2c637035b49ce5351a2617943684cd56a1b946740",
#   "address": "C1KHE58qD4FTzGHKKASBqPzsxrK9okr6SG",
#   "wif": "Br5oWwaMLuAx1TDZ5e9WcWfiVbzos6wf84wuMNNxgNbjvCUB6Dpj"
# }


# Only to be imported by bob.py
# Bob should have coins!!
bob_secret_key_BCY = CBitcoinSecret.from_secret_bytes(
    x('08d016b48ad5e970b0a56099a197dd78dbe57628f2eb19a3cee185cdb3b899b9'))
# {
#   "private": "08d016b48ad5e970b0a56099a197dd78dbe57628f2eb19a3cee185cdb3b899b9",
#   "public": "03ad6bd1a56e2fa4677b90377947645c2ff0feb53a4a6e86fd925008d9bbc6448f",
#   "address": "CCbDfAdViTrL3ecSmpqFtTr3pW2AUCuEKf",
#   "wif": "BodALYFRMsMfsZB2MKj33cnHRVn2KEWq7pK874ukh9eXBpnfPibJ"
# }

# "tx_ref": "3dc7f1ab40104cada91ed7d978baea4823bab1b31051810cb0c570a8a007faca" / CCbDfAdViTrL3ecSmpqFtTr3pW2AUCuEKf
# split 9x tran: 11be5bb6b7d0158fccc3958285f3e052c5f5d92902bca711909ed3917ca61c6e

# Can be imported by alice.py or bob.py
alice_public_key_BCY = alice_secret_key_BCY.pub
alice_address_BCY = P2PKHBitcoinAddress.from_pubkey(alice_public_key_BCY)
print('Alice_BCY', alice_address_BCY)
# Alice_BCY mohwwCB2rDB4gfzbNQQxZvrxqDxPbg2BUh

bob_public_key_BCY = bob_secret_key_BCY.pub
bob_address_BCY = P2PKHBitcoinAddress.from_pubkey(bob_public_key_BCY)
print('Bob_BCY', bob_address_BCY)
# Bob_BCY mzytNHfhMcmvk4Kiq4p2czi8gsfQ6fL5Gg

######################################################################
