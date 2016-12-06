#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import os
import time
import unittest

def mean(lst):
    num_items = len(lst)
    mean = sum(lst)/num_items
    
    return mean

def standard_deviation(lst):
    num_items = len(lst)
    mean = sum(lst)/num_items
    differences = [i - mean for i in lst]
    sq_differences = [d ** 2 for d in differences]
    ssd = sum(sq_differences)
    variance = ssd/num_items
    sd = math.sqrt(variance)
    
    return sd

class PerformanceTest(unittest.TestCase):
    def test_agentspeak_py(self):
        # FONTE: https://pymotw.com/2/subprocess/
        elapsed = []

        for i in range(100):
            start = time.time()
            os.system('python agentspeak-py/__main__.py maspy ../examples/print-var/printVar.maspy')
            done = time.time()
            difference = done - start        
            elapsed.append(difference)


        # print('')
        # print('Execuções: %s' % len(elapsed))
        # print('Média: %s segundos' % mean(elapsed))
        # print('Desvio Padrão: %s segundos' % standard_deviation(elapsed))
        # print('Tempo Total: %s segundos' % sum(elapsed))

        mean_value =  mean(elapsed)
        self.assertLess(mean_value, 0.065)

        # FONTE: http://jason.sourceforge.net/faq/#_how_to_run_my_application_without_jason_ide
        # Para o exemplo Room.maspy, criar no ambiente uma variável de controle que, com 100 interações, não continua.
        # Tanto para o Jason, quando para o AgentSpeak(Py).
        # http://campus.unibo.it/122397/9/4-jason.pdf

def main():
    unittest.main()

if __name__ == '__main__':
    main()