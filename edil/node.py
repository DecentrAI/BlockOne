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
@created on: Mon Jan 31 12:20:47 2022
@created by: damia
"""
import inspect
import numpy as np
from typing import List


from edil.utils import sample_shards

from edil.base import EDILBase
    

class SimpleWorker(EDILBase):
  def __init__(self, name, load, node, **kwargs):
    super().__init__(**kwargs)
    self.name = name
    self.load = load
    self.node = node
    

class ProcessingNode(EDILBase):
  
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    return
  
  
  def distributed_train(self, 
                        domain_encoder, # encoder that receives ndarray and returns ndarray
                        model_class, # class definition of the target model
                        model_weights_loader, # framework function for loading weights
                        model_weights_getter, # framework function for getting weights
                        train_data,  # training data tuple
                        dev_data,  # dev data tuple
                        test_data, # test data tuple
                        workers: List[SimpleWorker], rounds, # list of workers
                        train_class,
                        test_class,
                        aggregate_fn,
                        ):    
    # Distributed and semi-decentralized training

    assert inspect.isclass(train_class)
    assert inspect.isclass(test_class)
    assert inspect.isclass(model_class)
    
    

    # first encode data using pre-trained domain encoder
    x_train, y_train = train_data
    x_dev, y_dev = dev_data
    self.P("Using {:.2f} MB of train and dev data".format(
      sum([x.nbytes for x in [x_train, y_train, x_dev, y_dev]]) / 1024**2
      ))
    self.P("Running domain encoding...")
    enc_train = domain_encoder(x_train)
    enc_dev = domain_encoder(x_dev)
            
    n_train = len(enc_train)
    n_dev = len(enc_dev)
    self.P("  Encoded train: {} obs at {:.2f} MB out of {:.2f} MB".format(
      n_train,
      enc_train.nbytes / 1024**2,
      x_train.nbytes / 1024**2,
      ))
    self.P("  Encoded dev:   {} obs at {:.2f} MB out of {:.2f} MB".format(
      n_dev,
      enc_dev.nbytes / 1024**2,
      x_dev.nbytes / 1024**2,
      ))
        
    # get load per worker
    assert isinstance(workers[0], SimpleWorker)
    load_per_worker = [x.load for x in workers]
    if sum(load_per_worker)
    
    test_result_per_round = []
    
    # instantiate initial model
    model = model_class()
    
    # process multiple rounds of distributed training
    for idx_round in range(rounds):      
      train_per_worker = sample_shards(load_per_worker, n_obs=n_train)
      dev_per_worker = sample_shards(load_per_worker, n_obs=n_dev)
      model_states = []
      # load weights for current round
      starting_weights = model_weights_getter(model)
      for i, worker in enumerate(workers):
        worker_name = worker.name
        
        # now select only required training and dev shards
        worker_train_shard = train_per_worker[i]
        worker_x_train = enc_train[worker_train_shard]
        worker_y_train = y_train[worker_train_shard]

        worker_dev_shard = dev_per_worker[i]
        worker_x_dev = enc_dev[worker_dev_shard]
        worker_y_dev = y_dev[worker_dev_shard]
        # pass model, train/dev shards to worker
        model = worker.local_train(
          model_class=model_class, # send class not model
          model_weights=starting_weights, # the weights will be loaded from the state
          model_weights_loader=model_weights_loader,
          train_data=(worker_x_train, worker_y_train),
          dev_data=(worker_x_dev, worker_y_dev),
          test_class=test_class,
          train_class=train_class,
          )      
        model_states.append(model.state_dict())
      # aggregate model
      model = aggregate_fn(model, model_states)
      # test model
      if test_class is not None:
        test_func = test_class()
        test_result = test_func(model, test_data)
        test_result_per_round.append(test_result)
    return model
    
  
  def local_train(self, 
                  model_class, 
                  model_weights, 
                  model_weights_loader,
                  train, dev, 
                  train_class, 
                  dev_class, 
                  epochs, 
                  batch_size=32):
    assert inspect.isclass(train_class)
    assert inspect.isclass(dev_class)
    x_train, y_train = train
    train_func = train_class()
    dev_func = dev_class()
    model = model_class()
    model = model_weights_loader(model, model_weights)
    train_func(
      model=model, 
      x_train=x_train, 
      y_train=y_train, 
      epochs=epochs,
      dev_func=dev_func,
      dev_data=dev,
      )
    return model
  
  
if __name__ == '__main__':
  import torch as th
  from hfl.th_utils import aggregate_state_dicts
  
  class Base(th.nn.Module):
    def __init__(self):
      super().__init__()    
      self.l1 = th.nn.Linear(2,5)
      self.l2 = th.nn.Linear(5,2)
      
    def forward(self, inputs):
      x = self.l1(inputs)
      x = self.l2(x)
      return x
  
  
  class Adv(th.nn.Module):
    def __init__(self):
      super().__init__()
      self.m1 = Base()
      self.m2 = Base()
      self.ml = th.nn.ModuleList()
      self.ml.append(th.nn.Linear(3, 2))
      self.ml.append(th.nn.ReLU())
      self.ml.append(th.nn.Linear(2, 1))
      
    
    def forward(self, inputs):
      x = self.m1(inputs)
      x = self.m2(x)
      for layer in self.ml:
        x = layer(x)
      return x
  
  m1 = Adv()
  m2 = Adv()
  m3 = Adv()
  
  k1 = list(m1.state_dict().keys())[0]
  
  s1 = m1.state_dict()
  print("M1:\n{}".format(s1[k1]))
  s2 = m2.state_dict()
  print("M2:\n{}".format(s2[k1]))
  s3 = m3.state_dict()
  states = [s1,s2,s3]
  s = aggregate_state_dicts(states)
  print("AGG:\n{}".format(s[k1]))
  print("M1:\n{}".format(m1.state_dict()[k1]))
  