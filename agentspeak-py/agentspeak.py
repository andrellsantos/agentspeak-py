#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from unify import *

# Parse Literal
def parse_literal(content):
    literal = None
    # Se for string, quebra ela em literais
    if isinstance(content, str):
        regex_literal = '^\s*([~])?(\w*)[\(\s*]?([\w,\s]*)[\s*\)]?$'
        literal_content = re.findall(regex_literal, content)
        if literal_content:
            literal_content = literal_content.pop()
            # Negation
            negation = None
            negation_content = literal_content[0].strip()
            if negation_content:
                literal = Literal(negation_content)
            # Functor
            functor_content = literal_content[1].strip()
            functor = Literal(functor_content)
            if literal:
                literal.args = {functor}
            else:
                literal = functor
            # Arguments
            arguments = []
            arguments_content = literal_content[2].strip()   
            if arguments_content:
                arguments_content = re.split(',', literal_content[2].strip())          
                for argument_content in arguments_content:
                    argument_content = argument_content.strip()
                    arguments.append(Literal(argument_content))
                functor.args = arguments
    
    return literal

# Literal
class Literal(Expr):
    def __init__(self, functor, *args):
        Expr.__init__(self, functor, *args)
        self.functor = functor


# Crenças
class Belief:
    def __init__(self, content):
        # Se for string, quebra ela em literais
        if isinstance(content, str):
            self.expression = parse_literal(content)
        # Se for um conjunto de literais, popula direto a expressão
        elif isinstance(content, Literal):
            self.expression = content
        else:
            raise 'Parâmetro "content" declarado incorretamente na classe Belief'


    def __str__(self):
        return '%s' % self.expression

# Objetivos
class Goal:
    def __init__(self, content):
        # Se for string, quebra ela em literais
        if isinstance(content, str):
            goal = None
            regex_goals = '^\s*([\!\?])(.*)\s*$'
            goal_content = re.findall(regex_goals, content)
            if goal_content:
                goal_content = goal_content.pop()
                # Type
                type_content = goal_content[0].strip()
                goal = Literal(type_content)
                goal.args = {parse_literal(goal_content[1].strip())}
            self.expression = goal
        # Se for um conjunto de literais, popula direto a expressão
        elif isinstance(content, Literal):
            self.expression = content
        else:
            raise 'Parâmetro "content" declarado incorretamente na classe Goal'


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
        return '%s' % self.expression

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

# Ações
class Action:
    def __init__(self, agent_name, actions):
        self.agent_name = agent_name
        self.actions = actions
    
# Função .print()
class Print:
    def __init__(self, content):
        self.content = content

    def __str__(self):
        if self.content:
            return '.print("%s")' % self.content
        else:
            return '.print()'

# Função .send()
class Send:
    def __init__(self, destination, message):
        self.destination = destination
        self.message = message

    def __str__(self):
        return '.send(%s, %s)' % (self.destination, self.message)

# Mensagem da função .send()
class Message:
    def __init__(self, type, predicate):
        self.type = type
        self.predicate = predicate

    def __str__(self):
        return '%s, %s' % (self.type, self.predicate)

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
        if isinstance(context, str):
            self.context = self.__plan_context(context)

        # Corpo
        self.body = None
        if isinstance(body, str):
            self.body = self.__plan_body(body)
        
    def __str__(self):
        return '%s : %s <- %s' % (self.triggering_event, self.context, "; ".join(map(str, self.body)))

    # Contexto
    def __plan_context(self, context_content):
        belief = Belief(context_content)
        return belief.expression

    # Corpo
    def __plan_body(self, body_content):        
        body_content = re.split(';', body_content)
        plan_body = []        
        for content in body_content:           
            # Ações do tipo .print()
            print_actions = self.__plan_body_print(content.strip())
            plan_body.extend(print_actions)
            # Ações do tipo .send()
            send_actions = self.__plan_body_send(content.strip())
            plan_body.extend(send_actions)
            # # Outras ações
            other_actions = self.__plan_body_other(content.strip())
            plan_body.extend(other_actions)

        return plan_body

    # Ações do tipo .print()
    def __plan_body_print(self, content):
        print_actions = []
        # [TO-DO] Comentário
        regex_print = '^.print\((.*)\)$'
        prints_content = re.findall(regex_print, content, re.M)
        for print_content in prints_content:
            _print = Print(print_content[1:-1])
            print_actions.append(_print)

        return print_actions

    # Ações do tipo .send()
    def __plan_body_send(self, content):
        send_actions = []
        # [TO-DO] Verificar no Jason como os atributos do send() são definidos
        # [TO-DO] Comentário
        # regex_send = '^.send\((\w*),(\w*),[~!?]?(\w*)\((\w*)\)\)$'
        regex_send = '^.send\((\w*),(\w*),([\(\)~\w]*)\)$'
        sends_content = re.findall(regex_send, content, re.M)
        for send_content in sends_content:
            destination = send_content[0]
            type = send_content[1]
            predicate = send_content[2]
            # predicate = Literal(send_content[2].strip())
            # if send_content[3].strip():
                # predicate.args = {Literal(send_content[3].strip())}

            message = Message(type, predicate)
            send = Send(destination, message)
            send_actions.append(send)

        return send_actions

    # Outras ações
    def __plan_body_other(self, content):
        other_actions = []
        # [TO-DO] Comentário
        regex_action = '^(\w*)\(?([\w,]*)\)?$'
        actions_content = re.findall(regex_action, content, re.M)
        for action_content in actions_content:
            action = Literal(action_content[0].strip())
            if action_content[1].strip():
                action.args = {Literal(action_content[1].strip())}
            other_actions.append(action)

        return other_actions