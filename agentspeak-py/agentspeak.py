#!/usr/bin/python
# -*- coding: utf-8 -*-

class Term(object):
    pass
    
class Belief(object):
    pass
    
class Goal(object):
    pass
    
class AchievmentGoal(Goal):
    pass

class TestGoal(Goal):
    pass
    
class Action(object):
    pass
    
class TriggeringEvent(object):
    pass

# Belief Literals
class Context(object):
    pass

# Can be goals or actions
class Body(object):
    pass
    
class Plan(object):

    def __init__(self, triggering_event, context, body):
        pass

    def __str__(self):
        pass
