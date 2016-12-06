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
            event = Event(triggering_event, TRUE_INTENTION)
            self.__events.append(event)

        self.__messages = []
        self.__intentions = []

    def run(self, perceptions = [], messages = {}):
        # Função de verificação de mensagens
        self.__check_messages(messages)
        # Função de revisão de crenças (BRF)
        self.__belief_revision_function(perceptions)

        # Se não possuir nenhum elemento no conjunto de eventos ou conjunto de planos
        if not self.__events and not self.__intentions:
            return None

        relevant_plans = []
        while len(self.__events) > 0 and len(relevant_plans) == 0:
            # Função de seleção de evento
            event = self._event_selection()
            # Função de unificação para seleção dos planos relevantes
            relevant_plans = self.__unify_event(event)

        if relevant_plans:
            # Função de substituição para seleção dos planos relevantes
            applicable_plans = self.__unify_context(relevant_plans)
        
            if applicable_plans:
                # Função de seleção do plano pretendido
                intended_mean = self._intended_means_selection(applicable_plans)
                # Função de atualização do conjunto de intenções
                self.__update_intentions(intended_mean)

        # Função de selecão da intenção que será executada
        intention = self._intention_selection()

        # Função .print(belief_base)
        if intention and isinstance(intention, Action):
            if isinstance(intention.literal, Print) and not intention.literal.content:
                intention.literal.content = str(self.__belief_base)

        # Retorna a intenção que será executada no ambiente
        return intention

    # Função de verificação de mensagens
    def __check_messages(self, messages):
        self.__messages.extend(messages.pop(self.name, []))

        # Processa as mensagens recebidas
        # [TO-DO] Digamos que eu tenha diversas mensagens para um agente.. eu processo tudo no mesmo
        # ciclo de interpretação?
        for message in self.__messages:
            self.__process_messages(message.sender, message.type, message.literal)

        # Limpa a caixa de mensagens do agente
        self.__messages = []

    def __process_messages(self, sender, type, literal):
        # Tell
        # O agente que enviou a mensagem pretende que o agente receptor possua uma crença em que
        # o literal da mensagem seja verdadeiro.
        if type == 'tell':
            self.__belief_base.add(literal)
        # Untell
        # O agente que enviou a mensagem pretende que o agente receptor não possua uma crença em que
        # o literal da mensagem seja verdadeiro.
        elif type == 'untell':
            self.__belief_base.remove(literal)
        # Achieve
        # O agente que enviou a mensagem solicita que o agente receptor tente alcançar um estado 
        # em que o conteúdo do literal da mensagem seja verdadeiro, isto é, delegando um objetivo
        # para o agente receptor.
        elif type == 'achieve':
            goal = Goal('!' + literal)
            triggering_event = TriggeringEvent('+', goal)
            event = Event(triggering_event, TRUE_INTENTION)
            self.__events.append(event)
        # Unachieve
        # O agente que enviou a mensagem solicita que o agente receptor desista do objetivo de atingir
        # um estado em que o conteúdo do literal da mensagem seja verdadeiro.
        elif type == 'unachieve':
            goal = Goal('!' + literal)
            triggering_event = TriggeringEvent('-', goal)
            event = Event(triggering_event, TRUE_INTENTION)
            self.__events.append(event)
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
    def __belief_revision_function(self, perceptions):
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
            triggering_event = self.__belief_base.add(item)
            event = Event(triggering_event, TRUE_INTENTION)
            self.__events.append(event)

        # Cada literal da base de conhecimento que não está nas percepções é removido do conjunto de eventos
        remove_list = []
        for belief in self.__belief_base.items:
            if belief not in perceptions:
                remove_list.append(belief)

        for item in remove_list:
            triggering_event = self.__belief_base.remove(item)
            event = Event(triggering_event, TRUE_INTENTION)
            self.__events.append(event)

    # Função de seleção de evento
    def _event_selection(self):
        # Escolhe um único evento do conjunto de eventos
        event = None
        if self.__events:
            event = self.__events.pop(0)
        return event

    # Função de unificação para seleção dos planos relevantes
    def __unify_event(self, event):
        # Encontra os planos relevantes unificando os eventos ativadores com os cabeçalhos do conjunto de planos
        relevant_plans = []
        theta = {}
        for plan in self.__plan_library:
            unification = unify(event.triggering_event.literal, plan.triggering_event.literal, theta) 
            if unification != None:
                plan = self.__substitute_unifier(unification, plan)
                relevant_plans.append(plan)

        return relevant_plans
    
    # Função de substituição da unificação de um plano
    def __substitute_unifier(self, unification, plan):
        if len(unification) > 0:
            # Cria um cópia do plano
            plan = copy.deepcopy(plan)        
            # Realiza a substituição do evento arivador
            plan.triggering_event = substitute(unification, plan.triggering_event.literal)
            # Realiza a substituição do contexto
            plan_context = []
            for context in plan.context:
                plan_context.append(substitute(unification, context))
            plan.context = plan_context
            # Realiza a substituição do corpo
            plan_body = []
            for body in plan.body:
                if isinstance(body, Literal):
                    body = substitute(unification, body)
                elif isinstance(body, Goal):
                    body.content = substitute(unification, body.content)
                    body.literal = substitute(unification, body.literal)
                plan_body.append(body)
            plan.body = plan_body
        
        return plan

    # Função de substituição para seleção dos planos relevantes
    def __unify_context(self, relevant_plans):
        applicable_plans = []
        for plan in relevant_plans:
            if self.__relevant_unifier(plan.context):
                applicable_plans.append(plan)
                
        return applicable_plans
    
    def __unify_with_belief_base(self, content):
        theta = {}
        for belief in self.__belief_base.items:
            if unify(content, belief, theta) != None:
                return True

        return False

    def __relevant_unifier(self, context = []):
        if not context:
            return False
        if len(context) == 1:
            context = context[0]
            if context.functor == 'true':
                return True
            if context.functor == 'not':
                context = context.args[0]
                ret = self.__unify_with_belief_base(context)
                return not ret
            
            relevant_unifier = self.__unify_with_belief_base(context)
            return relevant_unifier
        else:
            relevant_unifier = self.__relevant_unifier(context[:1]) and self.__relevant_unifier(context[1:])
            return relevant_unifier

    # Função de seleção do plano pretendido
    def _intended_means_selection(self, applicable_plans):
        # Escolhe um único plano aplicável do conjunto de planos aplicáveis
        applicable_plan = None
        if applicable_plans:
            applicable_plan = applicable_plans.pop(0)
            # applicable_plan = random.choice(applicable_plans)

        return applicable_plan

    def __update_intentions(self, intended_mean):
        if intended_mean:
            intention = copy.deepcopy(intended_mean)
            self.__intentions.append(intention)

    # Função de selecão da intenção que será executada
    def _intention_selection(self):
        # Escolhe uma única intenção do conjunto de intenções
        intention = None
        while not intention:
            if self.__intentions:
                # Definição 13: Seleciona uma intenção i contida no topo do
                # conjunto de intenções I.
                intention = self.__intentions[-1]
                if intention.body:
                    copy_intention = copy.deepcopy(intention)
                    literal = intention.body.pop(0)
                    if isinstance(literal, Goal):
                        if literal.type == '!':
                            # Definição 13: Se a fórmula no corpo de 'i' for um objetivo de realização,
                            # um evento do tipo <+!g(t), i> é adicionado no conjunto de eventos e a
                            # intenção que gerou o evento é considerada executada
                            triggering_event = TriggeringEvent('+', copy.deepcopy(literal))
                            event = Event(triggering_event, copy_intention)
                            self.__events.append(event)
                            intention = True
                        elif literal.type == '?':
                            # Definição 14: No caso da fórmula do corpo da intenção 'i' ser um evento de
                            # teste, o conjunto de crenças é percorrido para encontrar um átomo de crenças
                            # que unifique o predicado de teste. Se encontrado, o objetivo é removido do
                            # conjunto de intenções, caso contrário, não executa os demais literias do corpo.
                            theta = {}
                            has_unification = False
                            for belief in self.__belief_base.items:
                                unification = unify(literal.content, belief, theta) 
                                if unification != None:
                                    has_unification = True
                                    break
                                
                            if has_unification:
                                intention = True
                            else:
                                self.__intentions.remove(intention)
                                intention = None
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