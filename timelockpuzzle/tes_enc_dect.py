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
@created on: Fri Sep 30 10:29:55 2022
@created by: damia
"""


import os
import sys

# line required to run as script (without -m option)
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from timelockpuzzle.puzzle_lib import encrypt


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Please time to encrypt, squarings per second, message')
    arg_t, arg_s, arg_message = sys.argv[1], sys.argv[2], sys.argv[3]

    p, q, n, a, t, encrypted_key, encrypted_message, key_int = encrypt(
        arg_message.encode(),
        int(arg_t),
        int(arg_s)
    )
    print(p, q, n, a, t, encrypted_key, encrypted_message.decode(), key_int)
    sys.stdout.flush()