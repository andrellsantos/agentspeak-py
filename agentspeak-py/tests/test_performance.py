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
    def test_print_var(self):
        elapsed = []

        for i in range(100):
            start = time.time()
            os.system('python agentspeak-py/__main__.py maspy ../examples/print-var/printVar.maspy')
            done = time.time()
            difference = done - start        
            elapsed.append(difference)

        mean_value =  mean(elapsed)
        self.assertLess(mean_value, 0.1)

def main():
    unittest.main()

if __name__ == '__main__':
    main()