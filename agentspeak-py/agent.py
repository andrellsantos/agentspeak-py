#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import copy
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
            self.__events.append(triggering_event.literal)

        self.__messages = []
        self.__intentions = []
    
    def run(self, perceptions = [], message_wall = {}):
        # Função de verificação de mensagens
        self.__checkMessageWall(message_wall)
        # Função de revisão de crenças (BRF)
        self.__beliefRevisionFunction(perceptions)
        
        # Se não possuir nenhum elemento no conjunto de eventos ou conjunto de planos
        if not self.__events and not self.__intentions:
            return None

        relevant_plans = []
        while len(self.__events) > 0 and len(relevant_plans) == 0:
            # Função de seleção de evento
            event = self._eventSelection()
            # Função de unificação para seleção dos planos relevantes
            relevant_plans = self.__unifyEvent(event)
        
        if relevant_plans:
            # Função de substituição para seleção dos planos relevantes
            applicable_plans = self.__unifyContext(relevant_plans)
        
            if applicable_plans:
                # Função de seleção do plano pretendido
                intended_mean = self._intendedMeansSelection(applicable_plans)
                # Função de atualização do conjunto de intenções
                self.__updateIntentions(intended_mean)
               
        # Função de selecão da intenção que será executada
        intention = self._intentionSelection()
        
        # Função .print(belief_base)
        if intention and isinstance(intention.literal, Print) and not intention.literal.content:
            intention.literal.content = str(self.__belief_base)
             
#         # Retorna a intenção que será executada no ambiente
        return intention
#         return None

    # Função de verificação de mensagens
    def __checkMessageWall(self, message_wall):
        self.__messages.extend(message_wall.pop(self.name, []))

        # Processa as mensagens recebidas
        # [TO-DO] Digamos que eu tenha diversas mensagens para um agente.. eu processo tudo no mesmo
        # ciclo de interpretação?
        for message in self.__messages:
            self.__processMessage(message.sender, message.type, message.literal)
            
        # Limpa a caixa de mensagens do agente
        self.__messages = []

    def __processMessage(self, sender, type, literal):
        # Tell
        if type == 'tell':
            raise 'O tipo \'tell\' está pendente de implementação na função .send()!'
        # Untell
        elif type == 'untell':
            raise 'O tipo \'untell\' está pendente de implementação na função .send()!'
        # Achieve
        elif type == 'achieve':
            goal = Goal('!' + literal)
            triggering_event = TriggeringEvent('+', goal)
            self.__events.append(triggering_event.literal)
        # Unachieve
        elif type == 'unachieve':
            goal = Goal('!' + literal)
            triggering_event = TriggeringEvent('-', goal)
            self.__events.append(triggering_event.literal)
        # AskOne
        elif type == 'askOne':
            raise 'O tipo \'askOne\' está pendente de implementação na função .send()!'
        # AskAll
        elif type == 'askAll':
            raise 'O tipo \'askAll\' está pendente de implementação na função .send()!'
        # TellHow
        elif type == 'tellHow':
            raise 'O tipo \'tellHow\' está pendente de implementação na função .send()!'
        # UntellHow
        elif type == 'untellHow':
            raise 'O tipo \'untellHow\' está pendente de implementação na função .send()!'
        # AskHow
        elif type == 'askHow':
            raise 'O tipo \'askHow\' está pendente de implementação na função .send()!'
        else:
            raise 'Tipo incorreto da função .send()!'

        # [TO-DO] Fazer (Página 118)

    # Função de revisão de crenças (BRF)
    def __beliefRevisionFunction(self, perceptions):
        # Recebe as informações provenientes do ambiente e as confronta com o seu conjunto de crenças
        # Caso as percepções do ambiente sejam diferentes, o conjunto de crenças é atualizado para que
        # reflitam o novo estado do ambiente
        # Cada crença modificada gera um novo evento que é adicionado no conjunto de eventos
        
        # Cada literal das percepções que não está na base de conhecimento é adicionado no conjunto de eventos
        remove_list = []
        for perception in perceptions:
            if perception not in self.__belief_base.items:
                remove_list.append(perception)

        for item in remove_list:
            self.__events.append(self.__belief_base.add(item))

        # Cada literal da base de conhecimento que não está nas percepções é removido do conjunto de eventos
        remove_list = []
        for belief in self.__belief_base.items:             
            if belief not in perceptions:
                remove_list.append(belief)

        for item in remove_list:
            self.__events.append(self.__belief_base.remove(item))

    # Função de seleção de evento
    def _eventSelection(self):
        # Escolhe um único evento do conjunto de eventos
        event = None
        if self.__events:
            event = self.__events.pop(0)
        return event


    # Função de unificação para seleção dos planos relevantes
    def __unifyEvent(self, event):
        # Encontra os planos relevantes unificando os eventos ativadores com os cabeçalhos do conjunto de planos
        relevant_plans = []
        theta = {}
        for plan in self.__plan_library:
            unification = unify(event, plan.triggering_event.literal, theta) 
            if unification != None:
                # self.substitution(plan, unification) - Return plan with substitution
                relevant_plans.append(plan)
        # [TO-DO] Fazer a substituição das variáveis
        # !start2(andre).
        # +!start2(A) : true <- mahalo(A).

        return relevant_plans

    # Função de substituição para seleção dos planos relevantes
    # [TO-DO] Dividir em uma função para obter o 'relevantUnifier'
    def __unifyContext(self, relevant_plans):
        theta = {}
        applicable_plans = []
        for plan in relevant_plans:
            has_breaked = False
            for context in plan.context:
                has_unification = False
                if has_breaked:
                    break

                if context.functor == 'true':
                    has_unification = True
                else:
                    if context.functor == 'not':
                        context = list(context.args)
                        if context:
                            has_unification = True
                            context = context.pop(0)
                            for belief in self.__belief_base.items:
                                if unify(context, belief, theta) != None:
                                    has_breaked = True
                                    break

                    else: 
                        for belief in self.__belief_base.items:    
                            if unify(context, belief, theta) != None:
                                has_unification = True
                                break
            
            if has_unification:
                applicable_plans.append(plan)
                
        return applicable_plans

    # Função de seleção do plano pretendido
    def _intendedMeansSelection(self, applicable_plans):
        # Escolhe um único plano aplicável do conjunto de planos aplicáveis
        applicable_plan = None
        if applicable_plans:
#             applicable_plan = applicable_plans.pop(0)
            applicable_plan = random.choice(applicable_plans)
        
        return applicable_plan

    def __updateIntentions(self, intended_mean):
        if intended_mean:
            intention = copy.deepcopy(intended_mean)
            self.__intentions.append(intention)

    # Função de selecão da intenção que será executada
    def _intentionSelection(self):
        # Escolhe uma única intenção do conjunto de intenções
        intention = None
        while not intention:
            if self.__intentions:
                # Definição 13: Seleciona uma intenção i contida no topo do
                # conjunto de intenções I.
                intention = self.__intentions[-1]
                intention_body = intention.body
                if intention_body:
                    literal = intention_body.pop(0)
                    
                    if isinstance(literal, Goal):                        
                        if literal.type == '!':
                            # Definição 13: Se a fórmula no corpo de 'i' for um objetivo de realização,
                            # um evento do tipo <+!g(t), i> é adicionado no conjunto de eventos  e a
                            # intenção que gerou o evento é considerada executada
                            print('Definição 13')                        
                        else:
                            # Definição 14: No caso da fórmula do corpo da intenção 'i' ser um evento de
                            # teste, o conjunto de crenças é percorrido para encontrar um átomo de crenças
                            # que unifique o predicado de teste. Se encontrado, o objetivo é removido do
                            # conjunto de intenções, pois foi realizado.
                            # [TO-DO] E se não for encontrado?
                            print('Definição 14')
                            
                    else:
                        # Definição 15: Se a fórmula no corpo da intenção 'i' for uma ação a ser realizada
                        # pelo agente no ambiente, o interpretador atualiza o estado do ambiente com a ação
                        # requerida e remove a ação do conjunto de intenções
                        intention = Action(self.name, literal)
                else:
                    self.__intentions.remove(intention)
                    intention = None
            else:
                break
        
        return intention
        
    def __str__(self):
        beliefs = "\n".join(str(belief) for belief in self.__belief_base)
        goals = "\n".join(str(goal) for goal in self.__initial_goals)
        plans = "\n".join(str(plan) for plan in self.__plan_library)

        return '[Name]\n%s\n[Belief Base]\n%s\n[Initial Goals]\n%s\n[Plan Library]\n%s\n' % (self.name, beliefs, goals, plans)
