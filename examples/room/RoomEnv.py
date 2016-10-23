#!/usr/bin/python
# -*- coding: utf-8 -*-

from environment import *

ld  = parse_literal('locked(door)')
nld = parse_literal('~locked(door)')


class RoomEnv(Environment):
    def __init__(self):
        Environment.__init__(self)
        self.add_percept(ld)

    def execute_action(self, agent_name, action):
        print("[%s] Doing %s" % (agent_name, action));
        self.clear_perceptions()

        getattr(self, action.functor)(action.args)

    def lock(self, *args):
        self.add_percept(ld)

    def unlock(self, *args):
        self.add_percept(nld)
        