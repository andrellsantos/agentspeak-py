#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
    Autor: André Santos
    Descrição: Classe responsável pelos ciclos de interpretação do AgentSpeak(Py).
    Realiza as interações entre os agentes e o ambiente após carregar as informações
    do projeto.
'''

from agent import *
from agentspeak import *
from environment import *
from project import *

class Interpreter:
    def __init__(self, file, debug = False, metrics = False, max_ticks = None):
        self.debug = debug
        self.metrics = metrics
        self.max_ticks = max_ticks
        # Carrega as informações do projeto
        project = Project(file)        
        # Define a lista dos agentes
        self.agents = project.agents        
        # Define o ambiente
        self.environment = project.environment        
                
    def run(self):
        # Contador com os cilos de interpretação
        ticks = 0
        # Variável de controle para parar as iterações e finalizar o interpretador
        wantFinish = False
        # Realiza as iterações enquanto que o usuário permitir
        while not wantFinish:
            # Pilha de ações provenientes do raciocínio dos agentes
            actions = []        
            # Atualiza as percepções de todos os agentes
            perceptions = []

            # Executa o ciclo de raciocínio dos agentes
            for agent in self.agents:
                action = agent.run(self.environment.perceptions, self.environment.message_wall)
                # Caso o agente queria executar uma ação no ambiente, adiciona na pilha de ações
                if action:
                    actions.append(action)

            # Executa a pilha de ações no ambiente
            if actions:
                for action in actions:
                    self.environment.execute(action)
            else:
                wantFinish = True

            if self.max_ticks and ticks > self.max_ticks:
                wantFinish = True

            # Incrementa o contador com os cliclos de interpretação
            ticks += 1
