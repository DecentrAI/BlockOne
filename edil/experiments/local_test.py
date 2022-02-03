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
@created on: Thu Feb  3 14:41:59 2022
@created by: damia


Algorithm:
  1. Get data
  2. Create multiple nodes
  3. Get a arbitrary node M and consider it as data owner
  4. Prepare M to have domain encoder and a model definition
  5. Send distributed job to other workers recording input vs received data size
  6. Monitor individual training results and overall results
  7. Finally aggregate domain + aggregated and test it

"""

from edil.node import ProcessingNode

from edil.experiments.data_utils import get_mnist_data


if __name__ == '__main__':
  
  
  
  (x_train, y_train), (x_dev, y_dev), (x_test, y_test) = get_mnist_data(as_numpy=True)
  
  w1 = ProcessingNode()
  w2 = ProcessingNode()
  w3 = ProcessingNode()
  w4 = ProcessingNode()
  