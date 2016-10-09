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
    theta = {}
    
    event = Expr('!', Expr('start'))

    
    beliefs = [Expr('!', Expr('start')), Expr('a', Expr('p')), Expr('~', Expr('a', Expr('p')))]

    # print(event)

    # for belief in beliefs:
    #    if unify(event, belief, theta) != None:
        #    print(belief)
    
    # unify_beliefs = [unify(event, belief, theta) for belief in beliefs]

    # P1 - triggering_event: +localizacao(lixo, X) : ...
    P1_triggering_event = Expr('+', Expr('localizacao', Expr('lixo'), Expr('X')))
    # P2 - triggering_event: +!localizacao(robo, X) : ...
    P2_triggering_event = Expr('+', Expr('!', Expr('localizacao', Expr('robo'), Expr('X'))))
    # P3 - triggering_event: +!localizacao(robo, X) : ...
    P3_triggering_event = Expr('+', Expr('!', Expr('localizacao', Expr('robo'), Expr('X'))))
    
    plans_triggering_event = [P1_triggering_event, P2_triggering_event, P3_triggering_event]

    # E: +!localizacao(robo, b)
    event = Expr('+', Expr('!', Expr('localizacao', Expr('robo'), Expr('b'))))

    # for triggering_event in plans_triggering_event:
    #    if unify(event, triggering_event, theta) != None:
        #    print(triggering_event)



    beliefs = [
        # Expr('locked', Expr('door'))
        # Expr('~', Expr('locked', Expr('door')))
        Expr('!', Expr('start')) 
        # Expr('a', Expr('p')), 
        # Expr('~', Expr('a', Expr('p')))
    ]

    # P1 - context: !start
    P1_context = Expr('true')
    # P2 - context: locked(door)
    # P2_context = Expr('~', Expr('locked', Expr('door')))

    plans_context = [P1_context]

    for context in plans_context:
        for belief in beliefs:
            if unify(context, belief, theta) != None:
               print(context)
