#!/usr/bin/python
# -*- coding: utf-8 -*-

import agentspeak

class Agent:
    def __init__(self, name, belief_base, initial_goals, plan_library):
        self.name = name
        self.__belief_base = belief_base
        self.__initial_goals = initial_goals
        self.__plan_library = plan_library

        self.__events = []
        self.__intentions = []
    
    def run(self, perceptions = None):
        print('Executando ciclo de raciocínio do agente %s...' % self.name)
        
        # Função de revisão de crenças (BRF)
        self.__beliefRevisionFunction(perceptions)
        # Escolhe um único evento do conjunto de eventos E
        event = self.__eventSelection()
        # Encontra os planos relevantes
        relevant_plans = self.__unifyEvent(event)
        # Encontra os planos aplicáveis a partir dos planos relevantes
        applicable_plans = self.__unifyContext(relevant_plans)
        # Opta pelo plano pretendido
        intended_mean = self.__intendedMeansSelection(applicable_plans)
        # Atualiza o conjunto de intenções I
        self.__updateIntentions(intended_mean)
        # Seleciona a intenção para ser executada
        intention = __intentionSelection()

        return intention

    def __beliefRevisionFunction(self, perceptions):
        pass

    def __eventSelection(self):
        # Remove e retorna o primeiro elemento da lista
        return self.__events.pop()

    def __unifyEvent(self, event):
        return None

    def __unifyContext(self, relevant_plans):
        return None

    def __intendedMeansSelection(self, applicable_plans):
        # Remove e retorna o primeiro elemento da lista
        return applicable_plans.left()

    def __updateIntentions(self, intended_mean):
       pass 

    def __intentionSelection(self):
        # Remove e retorna o primeiro elemento da lista
        return self.__intentions.pop()
        
    def __str__(self):
        beliefs = "\n".join(str(belief) for belief in self.__belief_base)
        goals = "\n".join(str(goal) for goal in self.__initial_goals)
        plans = "\n".join(str(plan) for plan in self.__plan_library)

        return '[Name]\n%s\n[Belief Base]\n%s\n[Initial Goals]\n%s\n[Plan Library]\n%s\n' % (self.name, beliefs, goals, plans)
