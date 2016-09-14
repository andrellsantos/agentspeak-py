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
from mas import *
from project import *

class Interpreter:

    def __init__(self):
        # Carrega as informações do projeto
        project = Project('/home/andre/Development/Python/agentspeak-py/examples/generic/generic.maspy')
        #project = Project('/home/PORTOALEGRE/13108260/DriveH/TCC/agentspeak-py/examples/generic/generic.maspy')
        
        # Define a lista dos agentes
        self.agents = project.agents
        
        # Embaralha os agentes 
        # [TO-DO] Quem possui a responsabilidade de definir as prioridades dos agentes?
        #         Criar classe com método base para ser sobrescrito quando o usuário
        #         desejar modificar a forma que são ordenados os agentes.
        # [FAIL] Eu não posso fazer assim... eu preciso carregar a classe informada no
        #        projeto (que deverá ser herdade de Mas) ou instanciar diretamente da
        #        classe Mas.
        mas = Mas(self.agents)
        mas.sort()
        self.agents = mas.agents
        
        # Define o ambiente
        self.environment = project.environment
        
        
    def run(self):
        # Contador com os cilos de interpretação
        tick = 0

        # Variável de controle para parar as iterações e finalizar o interpretador
        wantFinish = True

        # Pilha de ações provenientes do raciocínio dos agentes
        actions = []

        # Realiza as iterações enquanto que o usuário permitir
        while not wantFinish:
            # Atualiza as percepções de todos os agentes
    
            # Executa o ciclo de raciocínio dos agentes na
            for agent in self.agents:
                actions.append(agent.run())

            # Executa a pilha de ações 
            for action in actions:
                self.environment.execute(action)

            # Envia as mensagens para os agentes

            # Incrementa o contador com os cliclos de interpretação
            tick += 1

            if tick > 30:
                wantFinish = True
        
        
if __name__ == '__main__':
    interpreter = Interpreter()
    interpreter.run
