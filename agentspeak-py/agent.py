#!/usr/bin/python
# -*- coding: utf-8 -*-
# import copy
from agentspeak import *

class Agent:
    def __init__(self, name, belief_base, initial_goals, plan_library):
        self.name = name
        self.__belief_base = belief_base      
        # Conjunto de planos P
        self.__plan_library = plan_library
        # Conjunto de eventos E
        self.__events = []
        # Adiciona os objetivos iniciais no conjunto de eventos E
        for initial_goal in initial_goals:
            triggering_event = TriggeringEvent('+', initial_goal)
            self.__events.append(triggering_event.expression)

        self.__messages = []
        self.__intentions = []
    
    def run(self, perceptions = [], message_wall = {}):
        # print('Executando ciclo de raciocínio do agente %s...' % self.name)
        # Função de verificação de mensagens
        self.__checkMessageWall(message_wall)
        # Função de revisão de crenças (BRF)
        self.__beliefRevisionFunction(perceptions)
        # print('Nome do agente: %s' % self.name)
        # print(self.__events)
        # Se não possuir nenhum elemento no conjunto de eventos ou conjunto de planos
        if not self.__events or not self.__plan_library:
            return None
        # Função de seleção de evento
        event = self._eventSelection()
        # print('Evento: %s' % event)
        # Função de unificação para seleção dos planos relevantes
        relevant_plans = self.__unifyEvent(event)
        # Se nenhum plano relevante for selecionado
        if not relevant_plans:
            return None
        # Função de substituição para seleção dos planos relevantes
        applicable_plans = self.__unifyContext(relevant_plans)
        # Se nenhum plano aplicável for selecionado
        if not applicable_plans:
            return None            
        # Função de seleção do plano pretendido
        intended_mean = self._intendedMeansSelection(applicable_plans)
        # print('Plano pretendido: %s' % intended_mean)
        # Função de atualização do conjunto de intenções
        self.__updateIntentions(intended_mean)
        # Função de selecão da intenção que será executada
        intention = self._intentionSelection()

        # .print(belief_base)
        for action in intention.actions:
            if isinstance(action, Print) and not action.content:               
                action.content = str(self.__belief_base)

        # Retorna a intenção que será executada no ambiente
        return intention

    # Função de verificação de mensagens
    def __checkMessageWall(self, message_wall):
        self.__messages.extend(message_wall.pop(self.name, []))

        for message in self.__messages:
            self.__processMessage(message.type, message.predicate)

    def __processMessage(self, type, predicate):
        # Tell
        if type == 'tell':
            pass
        # Untell
        elif type == 'untell':
            pass
        # Achieve
        elif type == 'achieve':
            goal = Goal('!' + predicate)
            triggering_event = TriggeringEvent('+', goal.expression)
            self.__events.append(triggering_event.expression)
        # Unachieve
        elif type == 'unachieve':
            goal = Goal('!' + predicate)
            triggering_event = TriggeringEvent('-', goal.expression)
            self.__events.append(triggering_event.expression)
        # AskOne
        elif type == 'askOne':
            pass
        # AskAll
        elif type == 'askAll':
            pass
        # TellHow
        elif type == 'tellHow':
            pass
        # UntellHow
        elif type == 'untellHow':
            pass
        # AskHow
        elif type == 'askHow':
            pass
        else:
            raise 'Parâmetro incorreto da função .send()!'

        # [TO-DO] Fazer (Página 118)

    # Função de revisão de crenças (BRF)
    def __beliefRevisionFunction(self, perceptions):
        # Recebe as informações provenientes do ambiente e as confronta com o seu conjunto de crenças
        # Caso as percepções do ambiente sejam diferentes, o conjunto de crenças é atualizado para que
        # reflitam o novo estado do ambiente
        # Cada crença modificada gera um novo evento que é adicionado no conjunto de eventos
        
        # Cada literal das percepções que não está na base de conhecimento é adicionado no conjunto de eventos
        for perception in perceptions:
            if perception not in self.__belief_base.items:
                self.__events.append(self.__belief_base.add(perception))

        # Cada literal da base de conhecimento que não está nas percepções é removido do conjunto de eventos
        for belief in self.__belief_base.items:             
            if belief not in perceptions:
                self.__belief_base.remove(belief)
                # self.__events.append(self.__belief_base.remove(belief))
                

    # Função de seleção de evento
    def _eventSelection(self):
        # Escolhe um único evento do conjunto de eventos
        event = None
        if self.__events:
            event = self.__events.pop()
        return event

    # Função de unificação para seleção dos planos relevantes
    def __unifyEvent(self, event):
        # Encontra os planos relevantes unificando os eventos ativadores com os cabeçalhos do conjunto de planos
        relevant_plans = []
        theta = {}
        for plan in self.__plan_library:
            # print(event)
            # print(plan.triggering_event)
            # print(unify(event, plan.triggering_event, theta))
            if unify(event, plan.triggering_event, theta) != None:
                relevant_plans.append(plan)

        return relevant_plans

    # Função de substituição para seleção dos planos relevantes
    def __unifyContext(self, relevant_plans):
        theta = {}
        applicable_plans = []
        for plan in relevant_plans:
            if plan.context.functor == 'true':
                applicable_plans.append(plan)
            else:
                for belief in self.__belief_base.items:
                    if unify(plan.context, belief, theta) != None:
                        applicable_plans.append(plan)

        return applicable_plans

    # Função de seleção do plano pretendido
    def _intendedMeansSelection(self, applicable_plans):
        # Escolhe um único plano aplicável do conjunto de planos aplicáveis
        applicable_plan = None
        if applicable_plans:
            applicable_plan = applicable_plans.pop()
        
        return applicable_plan

    def __updateIntentions(self, intended_mean):
        if intended_mean:
            intention = intended_mean.body
            self.__intentions.append(intention)

    # Função de selecão da intenção que será executada
    def _intentionSelection(self):
        # Escolhe uma única intenção do conjunto de intenções
        intention = None
        if self.__intentions:
            intention = Action(self.name, self.__intentions.pop())
        
        return intention
        
    def __str__(self):
        beliefs = "\n".join(str(belief) for belief in self.__belief_base)
        goals = "\n".join(str(goal) for goal in self.__initial_goals)
        plans = "\n".join(str(plan) for plan in self.__plan_library)

        return '[Name]\n%s\n[Belief Base]\n%s\n[Initial Goals]\n%s\n[Plan Library]\n%s\n' % (self.name, beliefs, goals, plans)
