# -*- coding: utf-8 -*-
"""
Copyright 2019-2021 Lummetry.AI (Knowledge Investment Group SRL). All Rights Reserved.


* NOTICE:  All information contained herein is, and remains
* the property of Knowledge Investment Group SRL.  
* The intellectual and technical concepts contained
* herein are proprietary to Knowledge Investment Group SRL
* and may be covered by Romanian and Foreign Patents,
* patents in process, and are protected by trade secret or copyright law.
* Dissemination of this information or reproduction of this material
* is strictly forbidden unless prior written permission is obtained
* from Knowledge Investment Group SRL.


@copyright: Lummetry.AI
@author: Lummetry.AI
@project: 
@description:
@created on: Wed Mar 23 07:02:24 2022
@created by: damia
"""

from hashlib import sha256
import binascii

class BIP39:
  def __init__(self, file='utils/bip39.txt'):

    with open(file, 'rt') as fh:
      bip39words = fh.readlines()
    words = [x[:-1] for x in bip39words]
    
    bins = [self._bin(x, size=11) for x in range(len(words))]
    
    self.words = words
    self.bins = bins
    return
    
  def _bin(self, v, size):
    s = bin(v)[2:]
    s = '0' * (size - len(s)) + s
    return s
    
  def get_bin(self, word):
    try:
      idx = self.words.index(word)
      return self.bins[idx]
    except:
      return None
    
  def get_last_word(self, words):
    n_words = len(words)
    assert n_words in [11, 23]
    
    s_format = '%064x' if n_words == 24 else '%032x'

    size_checksum = (n_words + 1) // 3
    size_append = 11 - size_checksum
    bins = [self.get_bin(x) for x in words]
    if None in bins:
      idx = bins.index(None)
      raise ValueError("Word '{}' not in BIP39".format(words[idx]))
    concat = ''.join(bins)
    bin_options = [self._bin(x, size=size_append) for x in range(2**size_append)]
    results = []
    for bin_opt in bin_options:
      concated = concat + bin_opt
      value = int(concated, 2) 
      to_hash = binascii.unhexlify(s_format % value)
      h = sha256(to_hash).hexdigest()
      
      need_bytes = 2 if size_checksum > 4 else 1
      extr_prefix_hex = h[:need_bytes]
      int_extr = int(extr_prefix_hex, 16)      
      b_h = self._bin(int_extr, size=size_checksum)
      
      b_word = bin_opt + b_h
      assert len(b_word) == 11
      word_idx = int(b_word, 2)
      word = self.words[word_idx]      
      print(bin_opt,h, word)
      results.append(word)
    return results
    
  
    
    
    


if __name__ == '__main__':
  eng = BIP39()
  
  test24 = [
      'amount',
      'zero',
      'boat',
      'bone',
      'ceiling',
      'cake',
      'cause',
      'cost',
      'credit',
      'cupboard',
      'dinosaur',
      'dragon',
      'drum',
      'error',
      'fault',
      'fatal',
      'fog',
      'foam',
      'hold',
      'green',
      'hold',
      'join',
      'kick',
      ]
  
  test12 = [
    'salon', 
    'cup', 
    'frequent',
    'tank', 
    'second', 
    'swift', 
    'essay', 
    'already', 
    'melt', 
    'novel', 
    'creek', 
    #uncle    
    ]
  test12_2 = ['cash'] * 11
  test = test12_2
  res = eng.get_last_word(test)
  print(" ".join(test))
