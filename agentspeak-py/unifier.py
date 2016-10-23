#!/usr/bin/python
# -*- coding: utf-8 -*-

import platform
import re
import sys

if int(platform.python_version()[0]) < 3:
    sys.path.insert(0, './aima/python_2')  
    sys.path.insert(0, './agentspeak-py/aima/python_2')    
else:
    sys.path.insert(0, './aima/python_3')  
    sys.path.insert(0, './agentspeak-py/aima/python_3')

from logic import *

# Literal
class Literal(Expr):
    def __init__(self, functor, *args):
        Expr.__init__(self, functor, *args)
        self.functor = functor

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
            if literal_content[0].strip():
                literal = Literal(literal_content[0].strip())
            # Functor
            functor = Literal(literal_content[1].strip())
            if literal:
                literal.args = {functor}
            else:
                literal = functor
            # Arguments
            arguments = []
            arguments_content = literal_content[2].strip()
            if arguments_content:
                arguments_content = re.split(',', arguments_content)          
                for argument_content in arguments_content:
                    argument_content = argument_content.strip()
                    arguments.append(Literal(argument_content))
                functor.args = arguments

    return literal


def substitute(substitution, literal):
    if isinstance(literal, list):
        return [substitute(substitution, item) for item in literal]
    elif isinstance(literal, tuple):
        return tuple([substitute(substitution, item) for item in literal])
    elif not isinstance(literal, Literal):
        return literal
    elif is_var_symbol(literal.functor):
        return substitution.get(literal, literal)
    else:
        return Literal(literal.functor, *[substitute(substitution, arg) for arg in literal.args])


if __name__ == '__main__':
    theta = {}
    belief = Literal('!', Literal('start', Literal('andre')))
    triggering_event = Literal('!', Literal('start', Literal('A')))
 
    unification = unify(belief, triggering_event, theta)
    substitution = substitute(unification, triggering_event)
     
    print(substitution)