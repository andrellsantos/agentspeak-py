#!/usr/bin/python
# -*- coding: utf-8 -*-

# Literal
class Literal:
    def __init__(self, content):
        self.content = content

    def __str__(self):
        return '%s' % self.content    

# Predicados
class Predicate(Literal):
    pass
    
# Termos
class Term(Literal):
    pass
    
# Estrutura base para as crenças e objetivos
class Functor:
    def __init__(self, predicate, term = None):
        self.predicate = predicate
        self.term = term

    def __str__(self):
        if self.term == None:
            return '%s' % self.predicate
        else:
            return '%s(%s)' % (self.predicate, self.term)

# Crenças
class Belief(Functor):
    pass

# Objetivos
class Goal(Functor):
    pass

# Objetivos de realização
class AchievmentGoal(Goal):
    def __str__(self):
        return '!%s' % Goal.__str__(self)

# Objetivos de teste
class TestGoal(Goal):
    def __str__(self):
        return '?%s' % Goal.__str__(self)

# Ações
class Action(Functor):
    pass
    
# Eventos ativadores do plano - Podem ser crenças ou objetivos
class TriggeringEvent(Functor):
    pass

# Contexto do plano - Podem ser crenças ou 'true'
class Context(Functor):
    pass

# Corpo do plano - Pode ser objetivos ou ações
class Body(Functor):
    pass

# Plano
class Plan:
    # Tratar inicialmente como sendo uma string no contexto e no corpo
    # [TO-DO] Decompor o contexto e o corpo em uma lista de elementos
    # [TO-DO] Adicionar a fonte de recebimento do evento (Exemplo do paranóico)
    def __init__(self, type, triggering_event, context, body):
        self.type = type
        self.triggering_event = triggering_event
        self.context = context
        self.body = body

    def __str__(self):
        return '%s%s : %s <- %s' % (self.type, self.triggering_event, self.context, self.body)

