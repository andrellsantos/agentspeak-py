#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from agent import *
from agentspeak import *

class Parser:

    def __init__(self, file_name):
        agent_file = open(file_name, 'r');
        self.__load(agent_file.read())
        agent_file.close()

    def __load(self, agent_content):
        # [FERRAMENTA] https://regex101.com/#python
        # Remove o que está entre /* e */
        agent_content = re.sub('/\*.*\*/', '', agent_content, re.S)
        # Remove o que está após //
        agent_content = re.sub('//.*', '', agent_content)
        # Remove os espaços em branco
        # [FAIL] Não posso por causa das string dentro do .print ou .send
        # agent_content = re.sub(' ', '', agent_content)

        # Crenças
        # [belief(terms)]
        # (^[~]?\w*\(.*\))\.\s*$
        # [belief][(terms)]
        # ^([~]?\w*)\((.*)\)\.\s*$
        beliefs = []
        beliefs_content = re.findall('(^[~]?\w*\(.*\))\.\s*$', agent_content, re.M)
        for belief_content in beliefs_content:
            beliefs.append(belief_content)
            #print(belief_content)

        # Objetivos
        # [prefix goal(terms)]
        # ^([\!\?].*)\.\s*$
        # [prefix] [goal][(terms)]
        # ^([\!\?])([~]?\w*)\(?([\w,]*)\)?\.\s*$
        goals = []
        goals_content = re.findall('^([\!\?].*)\.\s*$', agent_content, re.M)
        for goal_content in goals_content:
            goals.append(goal_content)
            #print(goal_content)
        
        # Planos
        # [prefix] [event(terms)] : [context] <- [body]
        # ^([+-])(.*)\s*:\s*(.*)\s*<-\s*(.*)\s*\.\s*$
        # [prefix] event[(terms)] : [context] <- [body]
        # ^([+-])([\!]?)([~]?\w*)\(?([\w,]*)\)?(.*)\s*:\s*(.*)\s*<-\s*(.*)\s*\.\s*$
        plans = []
        plans_content = re.findall('^([+-])(.*)\s*:\s*(.*)\s*<-\s*(.*)\s*\.\s*$', agent_content, re.M)
        for plan_content in plans_content:
            plans.append(plan_content)
            #print(plan_content)
        
		
        # Cria o Agente
        self.agent = Agent(beliefs, goals, plans)
