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
@created on: Thu Feb  3 16:25:41 2022
@created by: damia
"""
import torch as th
import torchvision as tv

def get_mnist_data(dev):
  
  train = tv.datasets.MNIST(
    root='_cache', 
    train=True, 
    transform=tv.transforms.ToTensor(),
    download=True
    )
  full_test = tv.datasets.MNIST(
    root='_cache', 
    train=False, 
    transform=tv.transforms.ToTensor(),
    download=True
    )
  

  
  x_train = (train.data.view(-1,1,28,28) / 255.).to(dev)
  y_train = train.targets.to(dev)

  n_dev = full_test.data.shape[0] // 2

  x_dev = (full_test.data[:n_dev].view(-1,1,28,28) / 255.).to(dev)
  y_dev = full_test.targets[:n_dev].to(dev)

  x_test = (full_test.data[n_dev:].view(-1,1,28,28) / 255.).to(dev)
  y_test = full_test.targets[n_dev:].to(dev)

  return (x_train, y_train), (x_dev, y_dev), (x_test, y_test)
  