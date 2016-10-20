#!/usr/bin/python
# -*- coding: utf-8 -*-

from environment import *

class HelloWorldEnv(Environment):
    def __init__(self):
        Environment.__init__(self)

    def execute_action(self, agent_name, action):
        # self.agent_name = agent_name
        # print('[%s] Doing %s' % (agent_name, action));
        # self.add_percept(None)
        # self.clear_perceptions()

        eval('%s()' % action)

def aloha():
    print('Aloha HelloWorldEnv!')

def mahalo(argument):
    print('Mahaloing with %s' % argument)