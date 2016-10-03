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
    def __init__(self):
        # Carrega as informações do projeto
        project = Project('/home/andre/Development/Python/agentspeak-py/examples/generic/generic.maspy')
        # project = Project('/home/andre/Development/Python/agentspeak-py/examples/hello-world/helloWorld.maspy')
        # project = Project('/home/andre/Development/Python/agentspeak-py/examples/room/room.maspy')
        # project = Project('/home/PORTOALEGRE/13108260/DriveH/TCC/agentspeak-py/examples/generic/generic.maspy')
        
        # Define a lista dos agentes
        self.agents = project.agents        
        # Define o ambiente
        self.environment = project.environment        
                
    def run(self):
        # Número de agentes
        # print('Iniciando a execução do interpretador para %i agente(s).' % len(self.agents))
        # Contador com os cilos de interpretação
        tick = 0
        # Variável de controle para parar as iterações e finalizar o interpretador
        wantFinish = True
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

            # Incrementa o contador com os cliclos de interpretação
            tick += 1

        # print('Execução do interpretador finalizada após %i ciclos.' % tick)
        
        
if __name__ == '__main__':
    interpreter = Interpreter()
    interpreter.run
