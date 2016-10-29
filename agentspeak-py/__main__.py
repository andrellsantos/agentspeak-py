#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import sys
from interpreter import *

def main():
    # Linux
    # file = '/home/andre/Development/Python/agentspeak-py/examples/generic/generic.maspy'
    file = '/home/andre/Development/Python/agentspeak-py/examples/hello-world/helloWorld.maspy'
    # file = '/home/andre/Development/Python/agentspeak-py/examples/room/room.maspy'
    # file = '/home/andre/Development/Python/agentspeak-py/examples/open-world/openWorld.maspy'
    # Linux - PUC
    # file = '/home/PORTOALEGRE/13108260/DriveH/TCC/agentspeak-py/examples/generic/generic.maspy'

    # Windows
    # file = 'C:/Desenvolvimento/python/agentspeak-py/examples/hello-world/helloWorld.maspy'
    # file = 'C:/Desenvolvimento/python/agentspeak-py/examples/room/room.maspy'
    # file = 'C:/Desenvolvimento/python/agentspeak-py/examples/open-world/openWorld.maspy'
    
    # MAC
    # file = '/Users/mateusathaydesmartins/projects/agentspeak-py/examples/hello-world/helloWorld.maspy'
    # file = '/Users/mateusathaydesmartins/projects/agentspeak-py/examples/room/room.maspy'

    debug = False
    metrics = False
    max_ticks = None

    for arg in sys.argv:
        arguments = re.split('=', arg)
        if len(arguments) == 2:
            option = arguments[0].lower()
            value = arguments[1]
            if option != 'file':
                value = arguments[1].lower()
    
            if option == 'file':
                file = value
            elif option == 'debug':
                try:
                    if value == 'true':
                        debug = True
                    elif value != 'false':
                        raise
                except:
                    print('O argumento \'debug\' precisa ser um booleano (Ex.: debug=true).')
                    sys.exit(1)            
            elif option == 'metrics':
                try:
                    if value == 'true':
                        metrics = True
                    elif value != 'false':
                        raise
                except:
                    print('O argumento \'metrics\' precisa ser um booleano (Ex.: metrics=true).')
                    sys.exit(1)                    
            elif option == 'max_ticks':
                try:
                    max_ticks = int(value)
                except:
                    print('O argumento \'max_ticks\' precisa ser um inteiro (Ex.: max_ticks=50).')
                    sys.exit(1)
            else:
                print('O interpretador Agentspeak(py) permite apenas os argumentos \'file\', \'debug\', \'metrics\' e \'max_ticks\'.')
                sys.exit(1)


    # if len(sys.argv) == 1:
    #     print('O interpretador Agentspeak(py) permite apenas os argumentos \'file\', \'debug\', \'metrics\' e \'max_ticks\'.')
    #     sys.exit(1)

    interpreter = Interpreter(file, debug, metrics, max_ticks)
    interpreter.run()

if __name__ == '__main__':
    main()