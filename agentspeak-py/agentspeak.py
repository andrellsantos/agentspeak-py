#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from unify import *

# Literal
class Literal(Expr):
    def __init__(self, functor, *args):
        Expr.__init__(self, functor, *args)
        self.functor = functor
        self.arguments = args


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
            if literal_content[0].strip():
                literal = Literal(literal_content[0].strip())
            # Functor
            functor = Literal(literal_content[1].strip())
            if literal:
                literal.args = {functor}
            else:
                literal = functor
            # Arguments
            arguments = []
            arguments_content = literal_content[2].strip()
            if arguments_content:
                arguments_content = re.split(',', arguments_content)          
                for argument_content in arguments_content:
                    argument_content = argument_content.strip()
                    arguments.append(Literal(argument_content))
                functor.args = arguments
    
    return literal

# Crenças
class Belief:
    def __init__(self, content):
        if isinstance(content, str):
            self.expression = parse_literal(content)
        else:
            raise 'Parâmetro "content" declarado incorretamente na classe Belief'

    def __str__(self):
        return '%s' % self.expression


# Objetivos
class Goal:
    def __init__(self, content):
        if isinstance(content, str):
            self.type, self.content, self.expression = self.__parse(content)
        else:
            raise 'Parâmetro "content" declarado incorretamente na classe Goal'

    def __parse(self, content):
        type = None
        goal = None
        expression = None
        regex_goals = '^\s*([\!\?])(.*)\s*$'
        goal_content = re.findall(regex_goals, content)
        if goal_content:
            goal_content = goal_content.pop()
            type = goal_content[0].strip()
            goal = parse_literal(goal_content[1].strip())
            expression = Literal(type)
            expression.args = [goal]

        return type, goal, expression

    def __str__(self):
        return '%s' % self.expression

# Eventos ativadores do plano - Podem ser crenças ou objetivos
class TriggeringEvent:
    def __init__(self, type, content):
        self.type = type
        triggering_event = None
        
        if isinstance(type, str):
            triggering_event = Literal(type)
        else:
            raise 'Parâmetro "type" declarado incorretamente na classe TriggeringEvent'

        if isinstance(content, str):
            # Verifica se o evento ativador é uma crença
            belief = Belief(content)
            if belief.expression:
                triggering_event.args = [belief.expression]
        
            # Verifica se o evento ativador é um objetivo
            goal = Goal(content)
            if goal.expression:
                triggering_event.args = [goal.expression]

        elif isinstance(content, Literal):
            triggering_event.args = [content]
        elif isinstance(content, Belief):
            triggering_event.args = [content.expression]
        elif isinstance(content, Goal):
            triggering_event.args = [content.expression]
        else:
            raise 'Parâmetro "content" declarado incorretamente na classe TriggeringEvent'

        self.expression = triggering_event

    def __str__(self):
        return '%s' % self.expression

# Base de Crenças
class BeliefBase:
    def __init__(self, beliefs = []):
        self.items = beliefs

    def add(self, literal):
        self.items.append(literal)
        triggering_event = TriggeringEvent('+', literal)
        return triggering_event.expression
    
    def remove(self, literal):
        self.items.remove(literal)
        triggering_event = TriggeringEvent('-', literal)
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


if __name__ == '__main__':
    plan = Plan('+!start : true <- aloha; .print("Formas de imprimir a base de conhecimento:"); .print(); .print("").')
    print(plan.triggering_event.type)
    print(plan.triggering_event.content)
    print(plan.context)
    print(plan.body)

    pass