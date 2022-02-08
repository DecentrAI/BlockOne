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


Findings:
  - scaling is required for root=3
  - bigger batchsize yelds better results on root>3

"""


import torchvision as tv
import torch as th
import matplotlib.pyplot as plt

from edil.th_utils import SimpleDomainAutoEncoder, Trainer

def plot_grid(imgs1, imgs2, title):
  assert len(imgs1) == len(imgs2)
  fig, axs = plt.subplots(len(imgs1),2, figsize=(2,len(imgs1)))
  fig.suptitle(title)
  for i in range(len(imgs1)):
    axs[i][0].imshow(imgs1[i].squeeze())
    axs[i][0].axis('off')
    axs[i][1].imshow(imgs2[i].squeeze())
    axs[i][1].axis('off')
  plt.show()
  return

def test_func(model, test_data, tests=[1, 500], epoch=None, **kwargs):
  x_test, y_test = test_data
  th_slice = x_test[tests]
  np_slice = th_slice.detach().cpu().numpy()
  in_train = model.training
  model.eval()
  with th.no_grad():
    th_yh = model(th_slice)
    np_res = th_yh.cpu().numpy()
  title = "Epoch {}".format(epoch)
  plot_grid(np_slice, np_res, title)
  if in_train:
    model.train()
  return
  


if __name__ == '__main__':
  from edil.experiments.data_utils import get_mnist_data
  
  TRAIN_MODE = True
  TEST_MODE = False
  dev = th.device('cuda')
  (x_train, x_dev), (x_dev, y_dev), (x_test, y_test) = get_mnist_data(dev)
  
  train_data = th.utils.data.TensorDataset(x_train, x_train) 
  
  if TRAIN_MODE:
    ae = SimpleDomainAutoEncoder(
      h=28, w=28, channels=1, 
      domain_name='mnist',
      scale=3,
      )
    ae.to(dev)
    
    trainer = Trainer()
    trainer.P("Model:\n{}".format(ae))
    
    trainer(
      model=ae, 
      train_data=train_data, 
      dev_func=test_func, dev_data=(x_dev, y_dev), 
      epochs=10,
      batch_size=512,
      loss='mse'
      )
    
    ae.save_encoder()
    ae.save_decoder()
  
  if TEST_MODE:
    from edil.th_utils import SimpleImageEncoder, SimpleImageDecoder
    fn_enc = '_cache/encoder.pt'
    fn_dec = '_cache/decoder.pt'
    
    enc = SimpleImageEncoder(h=28, w=28, channels=1)
    enc.eval()
    enc.to(dev)
    enc.load_state_dict(th.load(fn_enc))
    th_enc = enc(x_test)
    
    dec = SimpleImageDecoder(embed_size=64, h=28, w=28, channels=1)
    enc.eval()
    dec.to(dev)
    dec.load_state_dict(th.load(fn_dec))
    th_dec = dec(th_enc).detach()
    
    tests = [10,100]
    gold = x_test.cpu().numpy()[tests]
    pred = th_dec.cpu().numpy()[tests]
    plot_grid(gold, pred)
    
    
  
  

