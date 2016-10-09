#!/usr/bin/python
# -*- coding: utf-8 -*-

from environment import *

class HelloWorldEnv(Environment):
    def __init__(self):
        Environment.__init__(self)

    def _execute_action(self, agent_name, action):
        self._add_percept(None)
        self._clear_perceptions()

        if action.functor == 'aloha':
            self.aloha()

    def aloha(self):
        print('Aloha HelloWorldEnv!')