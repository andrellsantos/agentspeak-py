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



# Parse Literal
def parse_literal(content):
    literal = None
    # Se for string, quebra ela em literais
    if isinstance(content, str):
        regex_literal = '^\s*([~])?(\w*)[\(\s*]?([\w,\s]*)[\s*\)]?$'
        literal_content = re.findall(regex_literal, content)
        if literal_content:
            literal_content = literal_content.pop()
            # Negation
            negation = None
            negation_content = literal_content[0].strip()
            if negation_content:
                literal = Literal(negation_content)
            # Functor
            functor_content = literal_content[1].strip()
            functor = Literal(functor_content)
            if literal:
                literal.args = {functor}
            else:
                literal = functor
            # Arguments
            arguments = []
            arguments_content = literal_content[2].strip()   
            if arguments_content:
                arguments_content = re.split(',', literal_content[2].strip())          
                for argument_content in arguments_content:
                    argument_content = argument_content.strip()
                    arguments.append(Literal(argument_content))
                functor.args = arguments
    
    return literal

# Literal
class Literal(Expr):
    def __init__(self, functor, *args):
        Expr.__init__(self, functor, *args)
        self.functor = functor

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