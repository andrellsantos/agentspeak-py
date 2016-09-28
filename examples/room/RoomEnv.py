#!/usr/bin/python
# -*- coding: utf-8 -*-

from environment import *

class RoomEnv(Environment):
    def __init__(self):
        Environment.__init__(self)

    def execute_action(self, action):
        self.add_percept(None)
        self.clear_perceptions()
        print('Hello RoomEnv!')