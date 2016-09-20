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

        # Crenças
        beliefs = self.__beliefs(agent_content)
        # Objetivos
        goals = self.__goals(agent_content)        
        # Planos
        plans = self.__plans(agent_content)		
        # Agente
        self.agent = Agent(agent_name, beliefs, goals, plans)

    # Crenças
    def __beliefs(self, agent_content):
        beliefs = []
        # [belief(terms)]
        # regex_beliefs = '(^[~]?\w*\(.*\))\.\s*$'
        # [belief][(terms)]
        regex_beliefs = '^([~]?\w*)\((.*)\)\.\s*$'
        beliefs_content = re.findall(regex_beliefs, agent_content, re.M)
        for belief_content in beliefs_content:
            predicate = Predicate(belief_content[0].strip())
            term = Term(belief_content[1].strip())
            # Crença
            belief = Belief(predicate, term)
            # Adiciona a crença na lista de crenças        
            beliefs.append(belief)

        return beliefs

    # Objetivos
    def __goals(self, agent_content):
        goals = []
        # [prefix goal(terms)]
        # regex_goals = '^([\!\?].*)\.\s*$'
        # [prefix] [goal][(terms)]
        regex_goals = '^([\!\?])([~]?\w*)\(?([\w,]*)\)?\.\s*$'
        goals_content = re.findall(regex_goals, agent_content, re.M)
        for goal_content in goals_content:
            # Objetivo de realização
            if goal_content[0] == '!':
                predicate = Predicate(goal_content[1].strip())
                term = None
                if goal_content[2].strip():
                    term = Term(goal_content[2].strip())
                # Objetivo de realização
                goal = AchievmentGoal(predicate, term)
            # Objetivo de teste
            else:
                predicate = Predicate(goal_content[1].strip())
                term = None
                if goal_content[2].strip():
                    term = Term(goal_content[2].strip())
                # Objetivo de teste
                goal = TestGoal(predicate, term)
            # Adiciona o objetivo na lista de objetivos
            goals.append(goal)

        return goals
    
    # Planos
    def __plans(self, agent_content):
        plans = []
        # [prefix] [event(terms)] : [context] <- [body]
        # regex_plans = '^([+-])(.*)\s*:\s*(.*)\s*<-\s*(.*)\s*\.\s*$'
        # [prefix] event[(terms)] : [context] <- [body]
        regex_plans = '^([+-])([\!]?)([~]?\w*)\(?([\w,]*)\)?(.*)\s*:\s*(.*)\s*<-\s*(.*)\s*\.\s*$'
        plans_content = re.findall(regex_plans, agent_content, re.M)
        for plan_content in plans_content:
            type = plan_content[0].strip()            
            # Evento ativador
            # Objetivo de realização
            if plan_content[1] == '!':
                predicate = Predicate(plan_content[2].strip())
                term = None
                if plan_content[3].strip():
                    term = Term(plan_content[3].strip())
                # Evento ativador
                triggering_event = AchievmentGoal(predicate, term)
            # Objetivo de teste
            elif plan_content[1] == '?':
                predicate = Predicate(plan_content[2].strip())
                term = None
                if plan_content[3].strip():
                    term = Term(plan_content[3].strip())
                # Evento ativador
                triggering_event = TestGoal(predicate, term)
            # Crença
            else:
                predicate = Predicate(plan_content[2].strip())
                term = Term(plan_content[3].strip())
                # Evento ativador
                triggering_event = Belief(predicate, term)

            # Contexto
            context = plan_content[5]
            # Corpo
            body = plan_content[6]
            # Plano
            plan = Plan(type, triggering_event, context, body)
            # Adiciona o plano na lista de planos
            plans.append(plan)

        return plans