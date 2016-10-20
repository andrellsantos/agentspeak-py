#!/usr/bin/python
# -*- coding: utf-8 -*-

from environment import *

class RoomEnv(Environment):
    ld  = parse_literal('locked(door)')
    nld = parse_literal('~locked(door)')

    def __init__(self):
        Environment.__init__(self)
        self.add_percept(self.ld)

    def execute_action(self, agent_name, action):
        print("[%s] Doing %s" % (agent_name, action));
        self.clear_perceptions()

        if action.functor == 'lock':
            self.add_percept(self.ld)
        
        if action.functor == 'unlock':
            self.add_percept(self.nld)

        