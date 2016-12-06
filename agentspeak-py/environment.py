#!/usr/bin/python
# -*- coding: utf-8 -*-

from agentspeak import *

# __all__ = ['execute', 'execute_action', 'clear_perceptions', 'add_perception']

class Environment:
    def __init__(self):
        # Percepções do ambiente
        self.perceptions = []
        self.messages = {}
    
    # Executa as ações no ambiente
    def execute(self, action):
        # .print()
        if isinstance(action.literal, Print):
            self.__print(action.agent_name, action.literal.content)
        # .send()
        elif isinstance(action.literal, Send):
            action.literal.message.sender = action.agent_name
            self.__send(action.literal.destination, action.literal.message)
        # Outras ações
        else:
            self.execute_action(action.agent_name, action.literal)

    # Imprime um conteúdo na tela
    def __print(self, agent_name, content):
        print('[%s] %s' % (agent_name, content))

    # Atualiza as mensagens dos agentes
    def __send(self, destination, message):
        messages = self.messages.get(destination, [])
        messages.append(message)
        
        self.messages[destination] = messages

    # Método que será sobrescrito pela classe personalizada de ambiente
    def execute_action(self, agent_name, action):
        pass

    def add_percept(self, literal):
        self.perceptions.append(literal)
        
    def clear_perceptions(self):
        self.perceptions = []

    def __str__(self):
        pass