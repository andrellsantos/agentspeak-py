#!/usr/bin/python
# -*- coding: utf-8 -*-

from environment import *

start_print = parse_literal('start_print(true)')

class HelloWorldEnv(Environment):
    def __init__(self):
        Environment.__init__(self)

    def execute_action(self, agent_name, action):
        self.clear_perceptions()

        getattr(self, action.functor)(list(action.args))

    def aloha(self, *args):
        self.add_percept(start_print)
        print('Aloha HelloWorldEnv!')

    def mahalo(self, *args):
        print('Mahaloing with %s!' % ", ".join(map(str, *args)))
