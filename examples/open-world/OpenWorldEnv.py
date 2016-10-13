#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
from environment import *

class OpenWorldEnv(Environment):    
    pa  = parse_literal("p(a)")
    pb  = parse_literal("p(b)")
    npa = parse_literal("~p(a)")
    npb = parse_literal("~p(b)")

    def __init__(self):
        Environment.__init__(self)
        
        self._add_percept(self.pa)
        self._add_percept(self.pb)
        self._add_percept(self.npa)
        self._add_percept(self.npb)
            
    def _execute_action(self, agent_name, action):
        self._clear_perceptions()

        if random.choice([True, False]):            
            self._add_percept(self.pa)

        if random.choice([True, False]):   
            self._add_percept(self.pb)
            
        if random.choice([True, False]):   
            self._add_percept(self.npa)
            
        if random.choice([True, False]):   
            self._add_percept(self.npb)


        