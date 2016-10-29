#!/usr/bin/python
# -*- coding: utf-8 -*-

# Importa as configurações para acesso aos módulos presentes na pasta 'agentspeak/'
import settings
import unittest
# Importa a classe responsável pelo ciclo de interpretação 'agentspeak/interpreter.py'
from interpreter import *


class InterpreterTest(unittest.TestCase):    
    def test_run(self):
        file = 'examples/hello-world/helloWorld.maspy'
        debug = False
        metrics = False
        max_ticks = None

        interpreter = Interpreter(file, debug, metrics, max_ticks)
        interpreter.run()

        self.assertTrue

def main():
    unittest.main()

if __name__ == '__main__':
    main()