#!/usr/bin/python
# -*- coding: utf-8 -*-

from agentspeak import *

class Environment:
    def __init__(self):
        # Percepções do ambiente
        self.clear_perceptions()
    
    # Executa as ações no ambiente
    def execute(self, actions):
        for action in actions:
            # .print()
            if isinstance(action, Print):
                self.__print(action.content)
            # .send()
            elif isinstance(action, Send):
                self.__send(action.destination, action, type, action.predicate)
            # Outras ações
            else:
                self.execute_action(action)

    # Imprime um conteúdo na tela
    def __print(self, content):
        print('%s' % content)

    # [TO-DO] Envia para o agente de destino o predicado de acordo com o tipo
    def __send(self, destination, type, predicate):
        print('[Enviar]\nDestino: %s\nTipo: %s\nPredicado: %s' % (destination, type, predicate))

    # Método que será sobrescrito pela classe personalizada de ambiente
    def execute_action(self, action):
        pass

    def add_percept(self, literal):
        self.perceptions.append(literal)

    def clear_perceptions(self):
        self.perceptions = []

    def __str__(self):
        pass