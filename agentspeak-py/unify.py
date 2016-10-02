#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import platform

if int(platform.python_version()[0]) < 3:
    sys.path.insert(0, './aima/python_2')    
else:
    sys.path.insert(0, './aima/python_3')


from logic import *

if __name__ == '__main__':    
    theta = {}
    #event = Expr('!start')
    #beliefs = [Expr('!start'), Expr('a', Expr('p')), Expr('~', Expr('a', Expr('p')))]

    # for belief in beliefs:
    #    if unify(event, belief, theta):
        #    print(belief)


    # P1: +localizacao(lixo, X) : ...
    P1 = Expr('+', Expr('localizacao', Expr('lixo'), Expr('X')))
    # P2: +!localizacao(robo, X) : ...
    P2 = Expr('+', Expr('!', Expr('localizacao', Expr('robo'), Expr('X'))))
    # P3: +!localizacao(robo, X) : ...
    P3 = Expr('+', Expr('!', Expr('localizacao', Expr('robo'), Expr('X'))))
    plans = [P1, P2, P3]

    # E: +!localizacao(robo, b)
    event = Expr('+', Expr('!', Expr('localizacao', Expr('robo'), Expr('b'))))

    # print(event)
    # print(plans)

    for plan in plans:
       if unify(event, plan, theta):
           print(plan)