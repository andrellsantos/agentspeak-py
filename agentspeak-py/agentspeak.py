#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from unify import *

# Literal
class Literal(Expr):
    pass

# Crenças
class Belief:
    def __init__(self, content):
        # Se for string, quebra ela em literais
        if isinstance(content, str):
            belief = None
            regex_beliefs = '^\s*([~])?(\w*)\(\s*(.*)\s*\)\s*$'
            belief_content = re.findall(regex_beliefs, content).pop()
            # Negation
            negation = None
            negation_content = belief_content[0].strip()
            if negation_content:
                belief = Literal(negation_content)
            # Functor
            functor_content = belief_content[1].strip()
            functor = Literal(functor_content)
            if belief:
                belief.args = {functor}
            else:
                belief = functor
            # Arguments
            arguments = []
            arguments_content = re.split(',', belief_content[2].strip())
            for argument_content in arguments_content:
                argument_content = argument_content.strip()
                arguments.append(Literal(argument_content))
            functor.args = arguments
            self.expression = belief
        # Se for um conjunto de literais, popula direto a expressão
        elif isinstance(content, Literal):
            self.expression = content
        else:
            raise 'Parâmetro "content" declarado incorretamente na  classe Belief'


    def __str__(self):
        return '%s' % self.expression

# Objetivos
class Goal:
    def __init__(self, content):
        # Se for string, quebra ela em literais
        if isinstance(content, str):
            goal = None
            regex_goals = '^\s*([\!\?])([~])?(\w*)\(?\s*([\w,\s]*)\s*\)?\s*$'
            goal_content = re.findall(regex_goals, content).pop()
            # Type
            type_content = goal_content[0].strip()
            goal = Literal(type_content)
            # Negation
            negation = None
            negation_content = goal_content[1].strip()
            if negation_content:
                negation = Literal(negation_content)
                goal.args = {negation}
            # Functor
            functor_content = goal_content[2].strip()
            functor = Literal(functor_content)
            if negation:
                negation.args = {functor}
            else:
                goal.args = {functor}
            # Arguments
            arguments = []
            arguments_content = goal_content[3].strip()
            if arguments_content:
                arguments_content = re.split(',', arguments_content)
                for argument_content in arguments_content:
                    argument_content = argument_content.strip()
                    arguments.append(Literal(argument_content))
                functor.args = arguments
            self.expression = goal
        # Se for um conjunto de literais, popula direto a expressão
        elif isinstance(content, Literal):
            self.expression = content
        else:
            raise 'Parâmetro "content" declarado incorretamente na  classe Goal'


    def __str__(self):
        return '%s' % self.expression

# Eventos ativadores do plano - Podem ser crenças ou objetivos
class TriggeringEvent:
    def __init__(self, type, content):
        triggering_event = None
        # Se for string, quebra ela em literais
        if isinstance(type, str):
            triggering_event = Literal(type)
        # Se for um conjunto de literais, popula direto a expressão
        elif isinstance(type, Literal):
            triggering_event = type
        else:
            raise 'Parâmetro "type" declarado incorretamente na classe TriggeringEvent'

        # Se for string, quebra ela em literais
        if isinstance(content, str):
            # Verifica se o evento ativador é uma crença
            regex_beliefs = '^\s*([~])?(\w*)\(\s*(.*)\s*\)\s*$'
            belief_content = re.findall(regex_beliefs, content)
            if belief_content:
                belief = Belief(content)
                triggering_event.args = {belief.expression}

            # Verifica se o evento ativador é um objetivo
            regex_goals = '^\s*([\!\?])([~])?(\w*)\(?\s*([\w,\s]*)\s*\)?\s*$'
            goal_content = re.findall(regex_goals, content)
            if goal_content:
                goal = Goal(content)
                triggering_event.args = {goal.expression}

        # Se for um conjunto de literais, popula direto a expressão
        elif isinstance(content, Literal):
            triggering_event.args = {content}

        else:
            raise 'Parâmetro "content" declarado incorretamente na classe TriggeringEvent'

        self.expression = triggering_event

    def __str__(self):
        return None

# Base de Crenças
class BeliefBase:
    def __init__(self, beliefs = []):
        self.items = beliefs

    def add(self, predicate):
        self.items.append(predicate)
        triggering_event = TriggeringEvent('+', predicate)
        return triggering_event.expression
    
    def remove(self, predicate):
        self.items.remove(predicate)
        triggering_event = TriggeringEvent('-', predicate)
        return triggering_event.expression

    def __str__(self):
        return '\n'.join(str(belief) for belief in self.items) 

# Contexto do plano - Podem ser crenças ou 'true'
class Context:
   pass

# Corpo do plano - Pode ser objetivos ou ações
class Body:
   pass

# # Ações
# class Action(Predicate):
#     pass
    
# # Imprimir
# class Print(Literal):
#     def __str__(self):
#         return '.print("%s")' % Literal.__str__(self)

# class Send:
#     def __init__(self, destination, type, predicate):
#         self.destination = destination
#         self.type = type
#         self.predicate = predicate

#     def __str__(self):
#         return '.send(%s, %s, %s)' % (destination, type, predicate)


# Plano
class Plan:
    def __init__(self, type, triggering_event, context, body):
        # Eventos ativadores
        self.triggering_event = None
        # Se for string, quebra ela em literais
        if isinstance(triggering_event, str):
            triggering_event = TriggeringEvent(type, triggering_event)
            self.triggering_event = triggering_event.expression
        # Se for um conjunto de literais, popula direto a expressão
        elif isinstance(triggering_event, Literal):
            self.triggering_event = Literal(type)
            self.triggering_event.args = {triggering_event}

        # Contexto
        self.context = None
        # Se for string, quebra ela em literais
        if isinstance(context, str):
            pass
        # Se for um conjunto de literais, popula direto a expressão
        elif isinstance(context, Literal):
            pass

        # Corpo
        self.body = None
        # Se for string, quebra ela em literais
        if isinstance(body, str):
            pass
        # Se for um conjunto de literais, popula direto a expressão
        elif isinstance(body, Literal):
            pass

    def __str__(self):
        return '%s : %s <- %s' % (self.triggering_event, self.context, self.body)