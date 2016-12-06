#!/usr/bin/python
# -*- coding: utf-8 -*-

# Importa as configurações para acesso aos módulos presentes na pasta 'agentspeak/'
import settings
import unittest
from agentspeak import *

class AgentSpeakTest(unittest.TestCase):
    # Crenças
    def test_belief(self):
        content = 'name(term)'
        belief = Belief(content)
        self.assertEqual(content, str(belief))

    # Objetivos de Realização
    def test_goal_achievement(self):
        self.assertTrue

    def test_goal_achievement_atom(self):
        self.assertTrue
    
    # Objetivos de Teste
    def test_goal_test(self):
        self.assertTrue

    def test_goal_test_atom(self):
        self.assertTrue

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