#!/usr/bin/python
# -*- coding: utf-8 -*-

from environment import *

st = parse_literal('show(true)')

class PrintBB(Environment):
    def __init__(self):
        Environment.__init__(self)
        self.add_percept(st)