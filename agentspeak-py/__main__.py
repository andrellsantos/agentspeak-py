import sys
from interpreter import *

if __name__ == '__main__':

    # file_name = '/home/andre/Development/Python/agentspeak-py/examples/generic/generic.maspy'
    # file_name = '/home/andre/Development/Python/agentspeak-py/examples/hello-world/helloWorld.maspy'
    file_name = '/home/andre/Development/Python/agentspeak-py/examples/room/room.maspy'
    # file_name = 'C:/Users/andre.santos/Downloads/agentspeak-py/examples/hello-world/helloWorld.maspy'
    # file_name = 'C:/Users/andre.santos/Downloads/agentspeak-py/examples/room/room.maspy'
    # file_name = '/home/PORTOALEGRE/13108260/DriveH/TCC/agentspeak-py/examples/generic/generic.maspy'

    debug_on = False
    max_ticks = None

    if sys.argv:
        if len(sys.argv) >= 4:
            try:
                max_ticks = int(sys.argv[3])
            except:
                print('O número máximo de interações precisa ser um número (argumento #3).')
                sys.exit(1)

        if len(sys.argv) >= 3:
            try:
                if sys.argv[2].lower() == 'true':
                    debug_on = True
                elif sys.argv[2].lower() != 'false':
                    raise
            except:
                print('O modo de debug precisa ser \'True\' ou \'False\' (argumento #2).')
                sys.exit(1)

        if len(sys.argv) >= 2:
            file_name = sys.argv[1]

    interpreter = Interpreter(file_name, debug_on, max_ticks)
    interpreter.run()
