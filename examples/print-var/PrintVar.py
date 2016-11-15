#!/usr/bin/python
# -*- coding: utf-8 -*-

from environment import *

ct = parse_literal('continue(execute)')

class PrintVar(Environment):
    def __init__(self):
        Environment.__init__(self)

    def execute_action(self, agent_name, action):
        self.clear_perceptions()

        getattr(self, action.functor)(list(action.args))

    def aloha(self, *args):
        self.add_percept(ct)
        print('Aloha printVar!')

    def mahalo(self, *args):
        print('Mahaloing with %s!' % ", ".join(map(str, *args)))
