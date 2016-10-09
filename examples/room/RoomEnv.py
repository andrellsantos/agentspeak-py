#!/usr/bin/python
# -*- coding: utf-8 -*-

from environment import *

class RoomEnv(Environment):
    ld  = parseLiteral('locked(door)')
    nld = parseLiteral('~locked(door)')

    def __init__(self):
        Environment.__init__(self)
        self._add_percept(self.ld)

    def execute_action(self, action):
        self._clear_perceptions()

        if action.getFunctor() == 'lock':
            self._add_percept(ld)
        
        if action.getFunctor() == 'unlock':
            self._add_percept(nld)

        