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
@created on: Tue Feb  1 18:05:37 2022
@created by: damia
"""


import torchvision as tv
import torch as th
import matplotlib.pyplot as plt

from hefl.th_utils import SimpleAutoEncoder, Trainer

def plot_grid(imgs1, imgs2):
  assert len(imgs1) == len(imgs2)
  fig, axs = plt.subplots(len(imgs1),2, figsize=(2,len(imgs1)))
  for i in range(len(imgs1)):
    axs[i][0].imshow(imgs1[i].squeeze())
    axs[i][0].axis('off')
    axs[i][1].imshow(imgs2[i].squeeze())
    axs[i][1].axis('off')
  plt.show()

def test_func(model, test_data, tests=[1, 500]):
  x_test, y_test = test_data
  th_slice = x_test[tests]
  np_slice = th_slice.detach().cpu().numpy()
  in_train = model.training
  model.eval()
  with th.no_grad():
    th_yh = model(th_slice)
    np_res = th_yh.cpu().numpy()
  plot_grid(np_slice, np_res)
  if in_train:
    model.train()
  return
  


if __name__ == '__main__':
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
  
  dev = th.device('cuda')
  
  x_train = (train.data.view(-1,1,28,28) / 255.).to(dev)
  train_data = th.utils.data.TensorDataset(x_train, x_train)
  
  n_dev = full_test.data.shape[0] // 2
  n_test = full_test.data.shape[0] - n_dev
  
  x_dev = (full_test.data[:n_dev].view(-1,1,28,28) / 255.).to(dev)
  y_dev = full_test.targets[:n_dev].to(dev)
  x_test = (full_test.data[n_dev:].view(-1,1,28,28) / 255.).to(dev)
  y_test = full_test.targets[n_dev:].to(dev)
  
  
  ae = SimpleAutoEncoder(h=28, w=28, channels=1)
  ae.to(dev)
  
  trainer = Trainer()
  
  trainer(
    model=ae, 
    train_data=train_data, 
    dev_func=test_func, dev_data=(x_dev, y_dev), 
    epochs=10,
    loss='mse'
    )
  
  ae.save_encoder()
  
  

