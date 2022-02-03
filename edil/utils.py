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
@created on: Tue Feb  1 08:57:24 2022
@created by: damia
"""

import numpy as np

def sample_shards(samples_per_batch, n_obs=100):
  results = []
  np_all = np.arange(n_obs)
  np_samples = np.array(samples_per_batch)
  if np_samples[0] < 1:
    assert np_samples.sum() == 1, "Sum of all batches must be 100% if percentages are given"
    np_samples = np_samples * n_obs
  np_samples = np_samples.astype('int32')
  np_avail = np.ones(n_obs).astype('bool')
  for batch_size in np_samples:
    np_candidates = np_all[np_avail]
    np_chosen = np.random.choice(np_candidates, size=batch_size, replace=False)
    np_chosen.sort()
    results.append(np_chosen)
    np_avail[np_chosen] = False
  return results


