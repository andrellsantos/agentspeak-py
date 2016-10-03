#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import os
from agent import *
from agentspeak import *

class Parser:
    def __init__(self, agent_name, file_name):
        agent_file = open(file_name, 'r');
        self.__load(agent_name, agent_file.read())
        agent_file.close()

    def __load(self, agent_name, agent_content):
        # [FERRAMENTA] https://regex101.com/#python
        # Remove o que está entre /* e */
        regex_multiple_comments = '/\*.*\*/'
        agent_content = re.sub(regex_multiple_comments, '', agent_content, re.S)
        # Remove o que está após //
        regex_comments = '//.*'
        agent_content = re.sub(regex_comments, '', agent_content)
        # Remove os espaços em branco
        # [FAIL] Não posso por causa das string dentro do .print ou .send
        # agent_content = re.sub(' ', '', agent_content)

        self.agent = None
        # Crenças
        belief_base = BeliefBase(self.__beliefs(agent_content))
        # Objetivos
        goals = self.__goals(agent_content)        
        # Planos
        plans = self.__plans(agent_content)		
        # Agente
        # self.agent = Agent(agent_name, belief_base, goals, plans)
        # print(belief_base)
        # print(goals)
        for plan in plans: print(plan)

    # Crenças
    def __beliefs(self, agent_content):
        beliefs = []
        # Beliefs: [~]functor(terms)
        regex_beliefs = '^\s*([~]?\w*\(.*\))\.\s*$'
        beliefs_content = re.findall(regex_beliefs, agent_content, re.M)
        for belief_content in beliefs_content:
            belief = Belief(belief_content)
            beliefs.append(belief.expression)

        return beliefs

    # Objetivos
    def __goals(self, agent_content):
        goals = []
        # Goals: [!|?][~]functor(terms)
        regex_goals = '^\s*([\!\?].*)\.\s*$'
        goals_content = re.findall(regex_goals, agent_content, re.M)
        for goal_content in goals_content:
            goal = Goal(goal_content)
            goals.append(goal.expression)

        return goals
    
    # Planos
    def __plans(self, agent_content):
        plans = []
        # Plans: [+|-] [event(terms)] : [context] <- [body]
        regex_plans = '^\s*([+-])(.*)\s*:\s*(.*)\s*<-\s*(.*)\s*\.\s*$'
        plans_content = re.findall(regex_plans, agent_content, re.M)
        for plan_content in plans_content:
            type = plan_content[0].strip()
            triggering_event = plan_content[1].strip()
            context = plan_content[2].strip()
            body = plan_content[3].strip()
            plan = Plan(type, triggering_event, context, body)
            plans.append(plan)

        return plans