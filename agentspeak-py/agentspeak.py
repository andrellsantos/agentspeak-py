#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from unifier import *

# Crenças
class Belief:
    def __init__(self, content):
        if isinstance(content, str):
            self.literal = parse_literal(content)
        else:
            raise 'Parâmetro "content" declarado incorretamente na classe Belief'

    def __str__(self):
        return '%s' % self.literal


# Objetivos
class Goal:
    def __init__(self, content):
        if isinstance(content, str):
            self.type, self.content, self.literal = self.__parse(content)
        else:
            raise 'Parâmetro "content" declarado incorretamente na classe Goal'

    def __parse(self, content):
        type = None
        goal = None
        literal = None
        regex_goals = '^\s*([\!\?])(.*)\s*$'
        goal_content = re.findall(regex_goals, content)
        if goal_content:
            goal_content = goal_content.pop()
            type = goal_content[0].strip()
            goal = parse_literal(goal_content[1].strip())
            literal = Literal(type)
            literal.args = [goal]

        return type, goal, literal

    def __str__(self):
        return '%s' % self.literal

# Eventos ativadores do plano - Podem ser crenças ou objetivos
class TriggeringEvent:
    def __init__(self, type, content):
        self.type = type
        self.literal = None
        
        if isinstance(type, str):
            self.literal = Literal(type)
        else:
            raise 'Parâmetro "type" declarado incorretamente na classe TriggeringEvent'

        if isinstance(content, str):
            # Verifica se o evento ativador é uma crença
            belief = Belief(content)
            if belief.literal:
                self.content = belief.literal
        
            # Verifica se o evento ativador é um objetivo
            goal = Goal(content)
            if goal.literal:
                self.content = goal.literal

        elif isinstance(content, Literal):
            self.content = content
        elif isinstance(content, Belief):
            self.content = content.literal
        elif isinstance(content, Goal):
            self.content = content.literal
        else:
            raise 'Parâmetro "content" declarado incorretamente na classe TriggeringEvent'
        
        self.literal.args = [self.content]

    def __str__(self):
        return '%s' % self.literal

# Base de Crenças
class BeliefBase:
    def __init__(self, beliefs = []):
        self.items = beliefs

    def add(self, literal):
        self.items.append(literal)
        triggering_event = TriggeringEvent('+', literal)
        return triggering_event
    
    def remove(self, literal):
        self.items.remove(literal)
        triggering_event = TriggeringEvent('-', literal)
        return triggering_event

    def __str__(self):
        return '\n'.join(str(belief) for belief in self.items) 

# Eventos
class Event:
    def __init__(self, triggering_event, intention):
        self.triggering_event = triggering_event
        self.intention = intention

    def __str__(self):
        return '%s | %s' % (self.triggering_event, self.intention)

# Ações
class Action:
    def __init__(self, agent_name, literal):
        self.agent_name = agent_name
        self.literal = literal

    def __str__(self):
        return self.literal

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
    def __init__(self, sender, type, literal):
        self.sender = sender
        self.type = type
        self.literal = literal

    def __str__(self):
        return '%s, %s' % (self.type, self.literal)

# Plano
class Plan:
    def __init__(self, content):
        if isinstance(content, str):
            self.content = content
            self.triggering_event, self.context, self.body = self.__parse(content)
        else:
            raise 'Parâmetro "content" declarado incorretamente na classe Plan'

    def __parse(self, content):
        triggering_event = None
        context = None
        body = None
        # Plans: [+|-] [event(terms)] : [context] <- [body]
        regex_plans = '^\s*([+-])(.*)\s*:\s*(.*)\s*<-\s*(.*)\s*$'
        plan_content = re.findall(regex_plans, content, re.M)

        if plan_content:
            plan_content = plan_content.pop()
            type_content = plan_content[0].strip()
            triggering_event_content = plan_content[1].strip()
            context_content = plan_content[2].strip()
            body_content = plan_content[3].strip()
            # Eventos ativadores
            triggering_event = TriggeringEvent(type_content, triggering_event_content)
            # Contexto
            context = self.__plan_context(context_content)
            # Corpo
            body = self.__plan_body(body_content)

        return triggering_event, context, body
        
    def __str__(self):
        context = []
        for item in self.context:
            if item.functor == 'not':
                item = list(item.args)
                if item:
                    item = item.pop()
                    context.append('not %s' % item)
            else:
                context.append(item)

        return '%s : %s <- %s' % (self.triggering_event, " & ".join(map(str, context)), "; ".join(map(str, self.body)))

    # Contexto
    def __plan_context(self, context_content):
        context_content = re.split('&', context_content)
        plan_context = []
        for content in context_content:
            content = content.strip()
            if content[0:3] == 'not':
                context = parse_literal('not')
                context.args = [parse_literal(content[4:])]
            else:
                context = parse_literal(content)
            plan_context.append(context)
        return plan_context

    # Corpo
    def __plan_body(self, body_content):
        body_content = re.split(';', body_content)
        plan_body = []
        for content in body_content:
            # [TO-DO] Melhorar... Fazer parecido com o TriggeringEvent
            # Ações do tipo .print()
            print_actions = self.__plan_body_print(content.strip())
            plan_body.extend(print_actions)
            # Ações do tipo .send()
            send_actions = self.__plan_body_send(content.strip())
            plan_body.extend(send_actions)
            # Outras ações
            other_actions = self.__plan_body_other(content.strip())
            plan_body.extend(other_actions)
            # Objetivos
            goal = Goal(content.strip())
            if goal.literal:
                plan_body.append(goal)

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
            sender = None
            type = send_content[1]
            literal = send_content[2]
            message = Message(sender, type, literal)
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
                action.args = [Literal(action_content[1].strip())]
            other_actions.append(action)

        return other_actions


TRUE_INTENTION = Plan('+!true : true <- true')

if __name__ == '__main__':
    pass
