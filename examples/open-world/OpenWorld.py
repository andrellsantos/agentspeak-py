#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
from environment import *

pa  = parse_literal("p(a)")
pb  = parse_literal("p(b)")
npa = parse_literal("~p(a)")
npb = parse_literal("~p(b)")
	
class OpenWorld(Environment):    

    def __init__(self):
        Environment.__init__(self)
        
        self.add_percept(pa)
        self.add_percept(pb)
        self.add_percept(npa)
        self.add_percept(npb)
            
    def execute_action(self, agent_name, action):
        self.clear_perceptions()

        if random.choice([True, False]):            
            self.add_percept(pa)

        if random.choice([True, False]):   
            self.add_percept(pb)
            
        if random.choice([True, False]):   
            self.add_percept(npa)
            
        if random.choice([True, False]):   
            self.add_percept(npb)