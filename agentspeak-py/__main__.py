#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import sys
from interpreter import *

def main():
    HELP = """Agentspeak(Py) maspy [debug] [max_ticks integer]
        maspy     - Arquivo maspy
        debug     - Ativar modo de deburação, padrão: desabilitado
        max_ticks - Executa um número inteiro de ciclos, padrão: ilimitado"""

    maspy = os.path.abspath(os.path.join(os.path.dirname(__file__), '../examples/hello-world/helloWorld.maspy'))
    debug = False
    max_ticks = None

    argv = sys.argv
    if argv:
        argv.pop(0)
    while argv:
        arg = argv.pop(0)
        if arg == 'maspy':
            try:
                maspy = argv.pop(0)
                maspy = os.path.abspath(os.path.join(os.path.dirname(__file__), maspy))
            except:
                print('esperado um argumento para maspy')
                sys.exit(1)
        elif arg == 'debug':
            debug = True
        elif arg == 'max_ticks':
            try:
                max_ticks = int(argv.pop(0))
            except:
                print('esperado um argumento inteiro para max_ticks')
                sys.exit(1)
        else:
            print('Argumento inválido: ' + arg)
            print(HELP)
            sys.exit(1)

    interpreter = Interpreter(maspy, debug, max_ticks)
    interpreter.run()

if __name__ == '__main__':
    main()