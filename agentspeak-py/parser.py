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
            functor = Functor(belief_content[0].strip())
            term = Term(belief_content[1].strip())
            # Crença
            belief = Belief(functor, term)
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
                functor = Functor(goal_content[1].strip())
                term = None
                if goal_content[2].strip():
                    term = Term(goal_content[2].strip())
                # Objetivo de realização
                goal = AchievmentGoal(functor, term)
            # Objetivo de teste
            else:
                functor = Functor(goal_content[1].strip())
                term = None
                if goal_content[2].strip():
                    term = Term(goal_content[2].strip())
                # Objetivo de teste
                goal = TestGoal(functor, term)
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
            # Tipo de evento ativador (adição ou remoção)
            type = plan_content[0].strip()            
            # Evento ativador
            triggering_event = self.__plan_triggering_event(plan_content[1].strip(), plan_content[2].strip(), plan_content[3].strip())
            # Contexto
            context = self.__plan_context(plan_content[5].strip())
            # Corpo
            body = self.__plan_body(plan_content[6].strip())
            # Plano
            plan = Plan(type, triggering_event, context, body)
            # Adiciona o plano na lista de planos
            plans.append(plan)

        return plans

    # Evento Ativador
    def __plan_triggering_event(self, type, functor_content, term_content):
        # Objetivo de realização
        if type == '!':
            functor = Functor(functor_content)
            term = None
            if term_content:
                term = Term(term_content)
            # Evento ativador
            triggering_event = AchievmentGoal(functor, term)
        # Objetivo de teste
        elif type == '?':
            functor = Functor(functor_content)
            term = None
            if term_content:
                term = Term(term_content)
            # Evento ativador
            triggering_event = TestGoal(functor, term)
        # Crença
        else:
            functor = Functor(functor_content)
            term = Term(term_content)
            # Evento ativador
            triggering_event = Belief(functor, term)

        return triggering_event

    # [TO-DO] Contexto
    def __plan_context(self, context_content):
        return context_content

    # Corpo
    def __plan_body(self, body_content):
        plan_body = []        
        # Ações do tipo .print()
        print_actions = self.__plan_body_print(body_content)
        plan_body.extend(print_actions)
        # Ações do tipo .send()
        send_actions = self.__plan_body_send(body_content)
        plan_body.extend(send_actions)
        # Outras ações
        other_actions = self.__plan_body_other(body_content)
        plan_body.extend(other_actions)

        return plan_body

    # Ações do tipo .print()
    def __plan_body_print(self, body_content):
        print_actions = []
        # [To-DO] Comentário
        regex_print = '^.print\("(.*)"\)$'
        prints_content = re.findall(regex_print, body_content, re.M)
        for print_content in prints_content:
            _print = Print(print_content)
            print_actions.append(_print)

        return print_actions

    # Ações do tipo .send()
    def __plan_body_send(self, body_content):
        send_actions = []
        # [To-DO] Comentário
        # regex_send = '^.send\((\w*),(\w*),(.*)\)$'
        regex_send = '^.send\((\w*),(\w*),(\w*\((\w*)\))\)$'
        sends_content = re.findall(regex_send, body_content, re.M)
        for send_content in sends_content:
            functor = Functor(send_content[2].strip())
            term = None
            if send_content[3].strip():
                term = Term(send_content[3].strip())
            action = Action(functor, term)
            send = Send(send_content[0], send_content[1], action)
            send_actions.append(send)

        return send_actions

    # Outras ações
    def __plan_body_other(self, body_content):
        other_actions = []
        # [To-DO] Comentário
        regex_action = '^\w*\(?([\w,]*)\)?$'
        actions_content = re.findall(regex_action, body_content, re.M)
        for action_content in actions_content:
            functor = Functor(action_content[0].strip())
            term = None
            if action_content[1].strip():
                term = Term(action_content[1].strip())
            action = Action(functor, term)
            other_actions.append(action)

        return other_actions