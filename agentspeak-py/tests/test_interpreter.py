#!/usr/bin/python
# -*- coding: utf-8 -*-

# Importa as configurações para acesso aos módulos presentes na pasta 'agentspeak/'
import settings
# Importa a classe responsável pelo ciclo de interpretação 'agentspeak/interpreter.py'
from interpreter import *


if __name__ == '__main__':
    interpreter = Interpreter()
    interpreter.run()