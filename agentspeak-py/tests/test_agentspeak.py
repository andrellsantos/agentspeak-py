#!/usr/bin/python
# -*- coding: utf-8 -*-

# Importa as configurações para acesso aos módulos presentes na pasta 'agentspeak/'
import settings
import unittest
from agentspeak import *

class AgentSpeakTest(unittest.TestCase):
    # Crenças
    def test_belief(self):
        belief = Belief('name(term)')

        self.assertEqual('name(term)', str(belief))

    # Objetivos de Realização
    def test_goal_achievement(self):
        goal = Goal('!name(term)')
        expected = ['!', 'name(term)', '!name(term)']
        result = [goal.type, str(goal.content), str(goal.literal)]

        self.assertListEqual(expected, result)

    def test_goal_achievement_atom(self):
        goal = Goal( '!name')
        expected = ['!', 'name',  '!name']
        result = [goal.type, str(goal.content), str(goal.literal)]

        self.assertListEqual(expected, result)
    
    # Objetivos de Teste
    def test_goal_test(self):
        goal = Goal('?name(term)')
        expected = ['?', 'name(term)', '?name(term)']
        result = [goal.type, str(goal.content), str(goal.literal)]

        self.assertListEqual(expected, result)

    def test_goal_test_atom(self):
        content = '?name'
        goal = Goal('?name')
        expected = ['?', 'name', '?name']
        result = [goal.type, str(goal.content), str(goal.literal)]

        self.assertListEqual(expected, result)

    # Eventos ativadores do plano - Podem ser crenças ou objetivos
    def test_triggering_event(self):
        self.assertTrue

    # Base de Crenças
    def test_belief_base(self):
        self.assertTrue

    # Eventos
    def test_event(self):
        self.assertTrue

    # Ações
    def test_action(self):
        self.assertTrue

    # Função .print()
    def test_print(self):
        self.assertTrue

    # Função .send()
    def test_send(self):
        self.assertTrue

    # Mensagem da função .send()
    def test_message(self):
        self.assertTrue

    # Plano
    def test_plan(self):
        self.assertTrue

def main():
    unittest.main()

if __name__ == '__main__':
    main()