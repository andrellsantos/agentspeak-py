#!/usr/bin/python
# -*- coding: utf-8 -*-

from agentspeak import *

class Environment:
    def __init__(self):
        # Percepções do ambiente
        self.perceptions = []
        self.message_wall = {}
    
    # Executa as ações no ambiente
    def execute(self, action):
        # .print()
        if isinstance(action, Print):
            self.__print(intention.agent_name, action.content)
        # .send()
        elif isinstance(action, Send):
            action.message.sender = intention.agent_name
            self.__send(action.destination, action.message)
        # Outras ações
        else:
            self._execute_action(intention.agent_name, action)

    # Imprime um conteúdo na tela
    def __print(self, agent_name, content):
        print('[%s] %s' % (agent_name, content))

    # Atualiza o quadro de mensagens dos agentes
    def __send(self, destination, message):
        messages = self.message_wall.get(destination, [])
        messages.append(message)
        
        self.message_wall[destination] = messages

    # Método que será sobrescrito pela classe personalizada de ambiente
    def _execute_action(self, action):
        pass

    def _add_percept(self, literal):
        self.perceptions.append(literal)
        
    def _clear_perceptions(self):
        self.perceptions = []

    def __str__(self):
        pass