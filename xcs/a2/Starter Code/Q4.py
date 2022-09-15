from bitcoin.core.script import *

######################################################################
# These functions will be used by Alice and Bob to send their respective
# coins to a utxo that is redeemable either of two cases:
# 1) Recipient provides x such that hash(x) = hash of secret
#    and recipient signs the transaction.
# 2) Sender and recipient both sign transaction
#
# TODO: Fill these in to create scripts that are redeemable by both
#       of the above conditions.
# See this page for opcode documentation: https://en.bitcoin.it/wiki/Script

# This is the ScriptPubKey for the swap transaction
def coinExchangeScript(public_key_sender, public_key_recipient, hash_of_secret):
    return [
        # fill this in!
        OP_IF, # check if OP_0 or OP_1
          OP_HASH160,
          hash_of_secret,
          OP_EQUALVERIFY, # fail if not of 
        OP_ELSE,
          public_key_sender,
          OP_CHECKSIGVERIFY,
        OP_ENDIF,
        # now that all if good we can send the transaction
        public_key_recipient,
        OP_CHECKSIG,
    ]

# This is the ScriptSig that the receiver will use to redeem coins
def coinExchangeScriptSig1(sig_recipient, secret):
    return [
        # fill this in!
        sig_recipient,
        secret,
        OP_1,
    ]

# This is the ScriptSig for sending coins back to the sender if unredeemed
def coinExchangeScriptSig2(sig_sender, sig_recipient):
    return [
        # fill this in!
        sig_recipient,
        sig_sender,
        OP_0,
    ]
######################################################################

######################################################################
#
# Configured for your addresses
#
# TODO: Fill in all of these fields
#

alice_txid_to_spend     = "2786afbdc7bc13f9ee5db84e97e2bde1aba37df3e32b94202a8e77919d785136"
alice_utxo_index        = 0
alice_amount_to_send    = 0.00001

bob_txid_to_spend       = "11be5bb6b7d0158fccc3958285f3e052c5f5d92902bca711909ed3917ca61c6e"
bob_utxo_index          = 0
bob_amount_to_send      = 0.0001

# Get current block height (for locktime) in 'height' parameter for each blockchain (will be used in swap.py):
#  curl https://api.blockcypher.com/v1/btc/test3
btc_test3_chain_height  = 2346276

#  curl https://api.blockcypher.com/v1/bcy/test
bcy_test_chain_height   = 455011

# Parameter for how long Alice/Bob should have to wait before they can take back their coins
# alice_locktime MUST be > bob_locktime
alice_locktime = 5
bob_locktime = 3

tx_fee = 0.0001

# While testing your code, you can edit these variables to see if your
# transaction can be broadcasted succesfully.
broadcast_transactions = False
alice_redeems = False

######################################################################
