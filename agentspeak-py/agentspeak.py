#!/usr/bin/python
# -*- coding: utf-8 -*-

# Literal
class Literal:
    def __init__(self, content):
        self.content = content

    def __str__(self):
        return '%s' % self.content    

# Functor
class Functor(Literal):
    pass
    
# Termos
class Term(Literal):
    pass
    
# Estrutura base para as crenças e objetivos
class Predicate:
    def __init__(self, functor, term = None):
        self.functor = functor
        self.term = term

    def __str__(self):
        if self.term == None:
            return '%s' % self.functor
        else:
            return '%s(%s)' % (self.functor, self.term)

# Crenças
class Belief(Predicate):
    pass

# Objetivos
class Goal(Predicate):
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
class Action(Predicate):
    pass
    
# Imprimir
class Print(Literal):
    def __str__(self):
        return '.print("%s")' % Literal.__str__(self)

class Send:
    def __init__(self, destination, type, predicate):
        self.destination = destination
        self.type = type
        self.predicate = predicate

    def __str__(self):
        return '.send(%s, %s, %s)' % (destination, type, predicate)


# Eventos ativadores do plano - Podem ser crenças ou objetivos
class TriggeringEvent:
    def __init__(self, type, predicate):
        self.type = type
        self.predicate = predicate

    def __str__(self):
        return '%s%s' % (self.type, self.predicate)

# Base de Crenças
class BeliefBase:
    def __init__(self, beliefs = []):
        self.items = beliefs

    def add(self, predicate):
        self.items.append(predicate)
        triggering_event = TriggeringEvent('+', predicate)
        return triggering_event
    
    def remove(self, predicate):
        self.items.remove(predicate)
        triggering_event = TriggeringEvent('-', predicate)
        return triggering_event

    def __str__(self):
        return "\n".join(str(belief) for belief in self.items) 

# Contexto do plano - Podem ser crenças ou 'true'
#class Context(Predicate):
#    pass

# Corpo do plano - Pode ser objetivos ou ações
#class Body(Predicate):
#    pass

# Plano
class Plan:
    # Tratar inicialmente como sendo uma string no contexto e no corpo
    # [TO-DO] Decompor o contexto e o corpo em uma lista de elementos
    # [TO-DO] Adicionar a fonte de recebimento do evento (Exemplo do paranóico)
    def __init__(self, triggering_event, context, body):
        self.triggering_event = triggering_event
        self.context = context
        self.body = body

    def __str__(self):
        return '%s : %s <- %s' % (self.triggering_event, self.context, self.body)

