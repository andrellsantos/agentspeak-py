#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
    Autor: André Santos
    Descrição: Classe responsável pelos ciclos de interpretação do AgentSpeak(Py).
    Realiza as interações entre os agentes e o ambiente após carregar as informações
    do projeto.
'''

import agent
import agentspeak
import environment

def run():
    # Carrega as informações do projeto
    
    # Define a lista dos agentes
    agents = []
    
    # Embaralha os agentes 
    # [TO-DO] Definir prioridades para os agentes
    
    # Define o ambiente
    environment    
    
    # Contador com os cilos de interpretação
    tick = 0
    
    # Variável de controle para parar as iterações e finalizar o interpretador
    wantFinish = False
    
    # Pilha de ações provenientes do raciocínio dos agentes
    actions = []
    
    # Realiza as iterações enquanto que o usuário permitir
    while not wantFinish:
        # Atualiza as percepções de todos os agentes
        
        # Executa o ciclo de raciocínio dos agentes na
        for agent in agents:
            actions.append(agent.run())
            
        # Executa a pilha de ações 
        for action in actions:
            environment.execute(action)
        
        # Envia as mensagens para os agentes
    
        print 'Ciclo:', tick
        
        # Incrementa o contador com os cliclos de interpretação
        tick += 1
        
        if tick > 30:
            wantFinish = True
        
        
if __name__ == '__main__':
    run()
