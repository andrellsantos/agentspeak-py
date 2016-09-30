#!/usr/bin/python
# -*- coding: utf-8 -*-

from environment import *

class HelloWorldEnv(Environment):
    def __init__(self):
        Environment.__init__(self)

    def execute_action(self, action):
        self.add_percept(None)
        self.clear_perceptions()

        if action.functor.content == 'aloha':
            self.aloha()

    def aloha(self):
        print('Hello HelloWorldEnv!')