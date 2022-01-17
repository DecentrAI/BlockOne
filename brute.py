# -*- coding: utf-8 -*-
"""
Copyright 2017-2021 Lummetry.AI (Knowledge Investment Group SRL). All Rights Reserved.
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
@author: Lummetry.AI - AID
@project:
@description:

"""
import threading
import time
from collections import deque

def match(a1, a2):
  addr_len = len(a1)
  trues = [a1[i] == a2[i] for i in range(addr_len)]
  return sum(trues)

class AddrFinder:
  def __init__(self, addr1, nr_threads, nr_matches):
    self.addr1 = addr1
    self.nr_threads = nr_threads  
    self._counter = 0
    self._nr_matches = nr_matches
    self.found = False
    self.msgs = deque(maxlen=100)
    self.stats = {}
    return
  
  def msg(self, s):
    self.msgs.append(s)
    return
  
  def run(self):
    print("Trying to brute-force find similar address with {}/{} matches".format(
      self._nr_matches, len(self.addr1)))
    for thr in range(self.nr_threads):
      job = threading.Thread(target=self._job, kwargs={'id_job':thr+1})
      job.start()
    while not self.found:
      time.sleep(1)        
      print('\rStatus @ {}: {}\r'.format(self._counter, self.stats), flush=True, end='')
      if len(self.msgs) > 0:
        print(self.msgs.popleft())
      
      
  def _job(self, id_job=0):
    local_counter = 0
    while not self.found:
      self._counter += 1
      local_counter += 1
      clnt = BlockOneClient('**', '*')
      a2 = clnt.address
      matches = match(self.addr1, a2)
      if matches >= self._nr_matches:
        self.found = True
        self.msg('\nThread {} found match at glocal/local iter {}/{}: {} vs {}'.format(
          id_job, self._counter, local_counter, self.addr1, a2))
      self.stats[id_job] = local_counter
    return