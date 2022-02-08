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
@created on: Tue Feb  1 08:57:01 2022
@created by: damia
"""
import numpy as np
import torch as th
import os


from edil.base import EDILBase


def weights_loader(model, dct_weights):
  model.load_state_dict(dct_weights)
  return model

def get_weights(model):
  return model.state_dict()
  


def aggregate_state_dicts(states):
  keys = [x for x in states[0]]
  n_states = len(states)
  for key in keys:
    for i in range(1, n_states):
      states[0][key] += states[i][key]
    states[0][key] /= n_states
  return states[0]


def th_aggregate(self, original, workers):
  state = aggregate_state_dicts(workers)
  original.load_state_dict(state)
  return state


class Trainer(EDILBase):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    return
  
  
  def __call__(self, **kwargs):
    self.train(**kwargs)
      
  def train(self, 
            model=None, 
            train_data=None,
            x_train=None, 
            y_train=None, 
            dev_func=None,
            dev_data=None,
            epochs=1, 
            batch_size=32,
            loss='cce', 
            optimizer='adam'):
    assert model is not None
    train_size = None
    if ((x_train is not None) and (y_train is not None)):
      th_ds = th.utils.data.TensorDataset(x_train, y_train)
      train_size = x_train.shape[0]
    elif train_data is not None and isinstance(train_data, th.utils.data.Dataset):        
      th_ds = train_data
      if isinstance(th_ds, th.utils.data.TensorDataset):
        train_size = th_ds.tensors[0].shape[0]
    else:
      raise ValueError('Please pass either x_train, y_train ndarrays or x_data torch Dataset')
    
    
    
    th_ldr = th.utils.data.DataLoader(
      dataset=th_ds,
      batch_size=batch_size
      )
    
    if loss.lower() == 'cce':
      loss_fn = th.nn.CrossEntropyLoss()
    elif loss.lower() == 'mse':
      loss_fn = th.nn.MSELoss()
    else:
      raise ValueError("Unknown loss function '{}'".format(loss))
      
    if optimizer.lower() == 'adam':
      opt = th.optim.Adam(model.parameters())
    else:
      raise ValueError("Unknown optimizer '{}'".format(optimizer))    
    if train_size is not None:
      nr_batches = train_size // batch_size 
      show_step =  nr_batches // 100
    dev_results = []
    for epoch in range(1, epochs + 1):
      if self.verbose:
        self.P("Epoch {}/{}...".format(epoch, epochs))
      model.train()
      losses = []
      for idx_batch, (th_x_batch, th_y_batch) in enumerate(th_ldr):
        th_yh = model(th_x_batch)
        th_loss = loss_fn(th_yh, th_y_batch)
        np_loss = th_loss.detach().cpu().numpy()
        losses.append(np_loss)
        opt.zero_grad()
        th_loss.backward()
        opt.step()
        if self.verbose and (train_size is not None) and (idx_batch % show_step) == 0:
          self.Pr("  Processed {:.1f}% - loss: {:.4f}".format(
            (idx_batch + 1) / nr_batches * 100,
            np_loss
            ))
      if self.verbose:
        self.P('  Epoch {} mean loss: {:.4f}{}'.format(epoch, np.mean(losses), ' ' * 50))
      if dev_func is not None and dev_data is not None:
        dev_res = dev_func(model, dev_data, epoch=epoch)
        dev_results.append(dev_res)
    dct_res = model.state_dict()
    return dct_res
  
  
class Tester(EDILBase):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    return
  
  def __call__(self, model, data, method='acc'):
    x_test, y_test = data
    in_training = model.training
    model.eval()
    with th.no_grad():
      th_yh = model(x_test)
      if method == 'acc':
        th_yp = th_yh.argmax(1)
        th_acc = (th_yp == y_test).sum() / y_test.shape[0]
      else:
        raise ValueError("Unknown testing method '{}'".format(method))
      res = th_acc.cpu().numpy()
    if self.verbose:
      self.P("{} result: {:.3f}".format(method, res))
    if in_training:
      model.train()
    return res
  
  
BASIC_ENCODER = [
  {
   "kernel"  : 3,
   "stride"  : 2,
   "filters" : 32,
   "padding" : 1
  },

  {
   "kernel"  : 3,
   "stride"  : 2,
   "filters" : 128,
   "padding" : 1,
  },
    
  {
   "kernel"  : 3,
   "stride"  : 1,
   "filters" : None, # this will be auto-calculated for last encoding layer
   "padding" : 1,
  },
  ]



class GlobalMaxPool2d(th.nn.Module):
  def __init__(self):
    super().__init__()
    return
  
  def forward(self, inputs):
    th_x = th.nn.functional.max_pool2d(
      inputs, 
      kernel_size=inputs.size()[2:]
      )
    th_x = th.squeeze(th.squeeze(th_x, -1), -1)
    return th_x
  
class ReshapeLayer(th.nn.Module):
  def __init__(self, shape):
    super().__init__()
    self._shape = shape
    return
  
  def __repr__(self):
    return self.__class__.__name__ + "{}".format(tuple([x for x in self._shape]))
  
  def forward(self, inputs):
    return inputs.view(-1, *self._shape)
  

class InputPlaceholder(th.nn.Module):
  def __init__(self, shape):
    super().__init__()
    self._shape = shape
    return
  
  def __repr__(self):
    return self.__class__.__name__ + "{}".format(tuple([x for x in self._shape]))
  
  def forward(self, inputs):
    return inputs
  
  
def calc_embed_size(h, w, c, root=3, scale=1):
  img_size = h * w * c
  v = int(np.power(img_size, 1/root))
  v = v * scale
  # now cosmetics
  vf = int(v / 4) * 4
  return vf
  
   

class SimpleImageEncoder(th.nn.Module):
  def __init__(self, h, w, channels,
               root=3, scale=1,
               layers=BASIC_ENCODER):
    super().__init__()
    self.hw = (h, w)
    self.layers = th.nn.ModuleList()
    last_channels = channels
    for layer in layers:
      k = layer.get('kernel', 3)
      s = layer.get('stride', 2)
      p = layer.get('padding', 1)
      f = layer['filters']
      if f is None:
        f = calc_embed_size(
          h, w, 
          c=channels,
          root=root,
          scale=scale
          )
      cnv = th.nn.Conv2d(
        in_channels=last_channels, 
        out_channels=f, 
        kernel_size=k,
        stride=s,
        padding=p,
        )
      last_channels = f
      bn = th.nn.BatchNorm2d(f)
      act = th.nn.ReLU()
      self.layers.append(cnv)
      self.layers.append(bn)
      self.layers.append(act)
    self.embed_layer = GlobalMaxPool2d()
    self.encoder_embed_size = last_channels
    return
  
  def forward(self, inputs):
    th_x = inputs
    for layer in self.layers:
      th_x = layer(th_x)
      # print('  ',th_x.shape)
    th_out = self.embed_layer(th_x)
    return th_out
  
  
class SimpleImageDecoder(th.nn.Module):
  def __init__(self, 
               h, w, 
               channels, 
               embed_size=None, 
               root=3,
               scale=1,
               layers=BASIC_ENCODER
               ):
    super().__init__()
    if embed_size is None:
      embed_size = calc_embed_size(
        h, w, 
        c=channels,
        root=root,
        scale=scale,
        )
    self.hw = (h, w)
    self.layers = th.nn.ModuleList()
    reduce_layers = len([x['stride'] for x in layers if x['stride'] > 1])
    input_layer = InputPlaceholder((embed_size,))
    expansion_channels = embed_size
    expansion_h = h // (2 ** reduce_layers)
    expansion_w = w // (2 ** reduce_layers)
    expansion_size = expansion_h * expansion_w * expansion_channels
    expansion_layer = th.nn.Linear(embed_size, expansion_size)
    reshape_layer = ReshapeLayer((
      expansion_channels,
      expansion_h, expansion_w
      ))
    self.layers.append(input_layer)
    self.layers.append(expansion_layer)
    self.layers.append(reshape_layer)
    last_channels = expansion_channels
    layers.reverse()
    for layer in layers:
      k = layer.get('kernel', 3)
      s = layer.get('stride', 2)
      p = layer.get('padding', 1)
      f = layer['filters']
      if f is None:
        f = embed_size
      if s == 1:
        cnv = th.nn.Conv2d(
          in_channels=last_channels, 
          out_channels=f, 
          kernel_size=k,
          stride=1,
          padding=p
          )
      else:
        cnv = th.nn.ConvTranspose2d(
          in_channels=last_channels, 
          out_channels=f, 
          kernel_size=k-1,
          stride=s,
          # padding=p
          )
      last_channels = f
      bn = th.nn.BatchNorm2d(f)
      act = th.nn.ReLU()
      self.layers.append(cnv)
      self.layers.append(bn)
      self.layers.append(act)
    self.out_layer = th.nn.Conv2d(last_channels, channels, kernel_size=1)
    return
  
  def forward(self, inputs):
    th_embed = inputs
    th_x = th_embed
    for layer in self.layers:
      th_x = layer(th_x)
      # print('  ',th_x.shape)
    th_out = self.out_layer(th_x)
    return th_out
      
    
    
class SimpleDomainAutoEncoder(th.nn.Module):
  def __init__(self, 
               h, w, channels,
               domain_name,
               save_folder='_cache',
               root=3,
               scale=1,
               layers=BASIC_ENCODER
               ):
    super().__init__()
    
    self.domain_name = domain_name
    self.save_folder = save_folder
    
    self.encoder = SimpleImageEncoder(
      h=h, w=w, 
      channels=channels,
      layers=layers,
      root=root,
      scale=scale,
      )
    
    self.decoder = SimpleImageDecoder(
      embed_size=self.encoder.encoder_embed_size, 
      h=h, w=w, 
      channels=channels,
      layers=layers
      )
    return
  
  def forward(self, inputs):
    th_x = self.encoder(inputs)
    th_out = self.decoder(th_x)
    return th_out
  
  
  def save_encoder(self, path=None):
    if path is None:
      path = os.path.join(
        self.save_folder, 
        "{}_enc{}.pt".format(
          self.domain_name,
          self.encoder.encoder_embed_size
          )
        )
    in_train = self.encoder.training
    self.encoder.eval()
    th.save(self.encoder.state_dict(), path)
    self.encoder_save_path = path
    if in_train:
      self.encoder.train()
    return
  
  def save_decoder(self, path=None):
    if path is None:
      path = os.path.join(
        self.save_folder, 
        "{}_dec{}.pt".format(
          self.domain_name,
          self.encoder.encoder_embed_size
          )
        )
    in_train = self.decoder.training
    self.decoder.eval()
    th.save(self.decoder.state_dict(), path)
    self.decoder_save_path = path
    if in_train:
      self.decoder.train()
    return
    
    
    

if __name__ == '__main__':
  import numpy as np
  H = 28
  h, w = H, H
  enc = SimpleImageEncoder(h=h, w=w, channels=3)
  print('*****************************')
  print(enc)
  th_x = th.tensor(np.random.randint(0,255, size=(2, 3, h, w)), dtype=th.float32)
  th_yh = enc(th_x)
  print(th_yh.shape)
  # ae = SimpleAutoEncoder(h=h, w=w)
  # print(ae)
  
  dec = SimpleImageDecoder(th_yh.shape[1], h, w, channels=3)
  print('*****************************')
  print(dec)
  th_im = dec(th_yh)
  print(th_im.shape)
  
  ae = SimpleDomainAutoEncoder(h=h, w=w, channels=3)
  th_im = ae(th_x)
  print('*****************************')
  print(ae)
  print(th_im.shape)
  