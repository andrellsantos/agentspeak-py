#!/usr/bin/python
# -*- coding: utf-8 -*-

from environment import *

class RoomEnv(Environment):
    ld  = parse_literal('locked(door)')
    nld = parse_literal('~locked(door)')

    def __init__(self):
        Environment.__init__(self)
        self._add_percept(self.ld)

    def _execute_action(self, agent_name, action):
        print("Agent %s is doing %s" % (agent_name, action));
        self._clear_perceptions()

        if action.functor == 'lock':
            self._add_percept(self.ld)
        
        if action.functor == 'unlock':
            self._add_percept(self.nld)

        