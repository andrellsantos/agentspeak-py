#!/usr/bin/python
# -*- coding: utf-8 -*-

import agentspeak

class Agent:

    def __init__(self, beliefs, goals, plans):
        self.beliefs = beliefs
        self.goals = goals
        self.plans = plans
    
    def run(self):
        print('Executando ciclo de raciocínio do agente...')
    
    
    def __str__(self):
        pass
