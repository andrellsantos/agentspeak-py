#!/usr/bin/python
# -*- coding: utf-8 -*-

from agentspeak import *

class Environment:
    def __init__(self):
        pass
    
    def execute(self, actions):
        for action in actions:
            if isinstance(action, Print):
                self.__print(action.content)
            elif isinstance(action, Send):
                self.__send(action.destination, action, type, action.predicate)

    def __print(self, content):
        print('[Imprimir] "%s"' % content)

    def __send(self, destination, type, predicate):
        print('[Enviar]\nDestino: %s\nTipo: %s\nPredicado: %s' % (destination, type, predicate))

    def __str__(self):
        pass