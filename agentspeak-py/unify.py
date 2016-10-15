#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import platform

if int(platform.python_version()[0]) < 3:
    sys.path.insert(0, './aima/python_2')  
    sys.path.insert(0, './agentspeak-py/aima/python_2')    
else:
    sys.path.insert(0, './aima/python_3')  
    sys.path.insert(0, './agentspeak-py/aima/python_3')

from logic import *

if __name__ == '__main__':
    #Literais a serem testados
    # locked(door)
    # ~locked(door)
    # !start
    # localizacao(lixeira, b)
    # deliver(Product, Qtd)
    # delivered(Product, Qtd, OrderId)
    # check(locked(door))
    # check(locked(door), ~locked(door))
    # check(locked(door), ~locked(door), true)

    pass