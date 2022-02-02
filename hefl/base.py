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
@created on: Wed Feb  2 08:12:25 2022
@created by: damia
"""

from datetime import datetime

def _P(s):
  print(s, flush=True)

def _Pr(s):
  print("\r" + s + "\r", flush=True, end='')

def get_shortname(s):
  return "".join([x for x in s if x.isupper()])


class HEFLBase:
  def __init__(self, use_prefix=None, verbose=True):
    self.verbose = verbose
    if use_prefix is None:
      use_prefix = get_shortname(self.__class__.__name__)
    self._prefix = use_prefix
    return
  
  def _prep_str(self, s):
    s = '[{}][{}] {}'.format(
      self._prefix,
      datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
      s
      )
    return s


  def P(self, s):
    _P(s)
    return


  def Pr(self, s):
    _Pr(s)
    return
  
    