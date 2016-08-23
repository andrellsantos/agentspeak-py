import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import interpreter

if __name__ == '__main__':
    interpreter.run()