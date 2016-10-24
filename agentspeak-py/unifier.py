#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

# Literal
class Literal:
    def __init__(self, functor, *args):
        self.functor = str(functor)
        self.args = args

    def __call__(self, *args):
        assert is_symbol(self.functor) and not self.args
        return Literal(self.functor, *args)

    def __repr__(self):
        functor = self.functor
        args = [str(arg) for arg in self.args]
        if is_symbol(functor):
            # return '%s(%s)' % (self.functor, ', '.join(map(repr, self.args)))
            return '{}({})'.format(functor, ', '.join(args)) if args else functor
        elif len(args) == 0:
            return functor
        elif len(args) == 1:
            return functor + args[0]
        else:
            return '(' + (' ' + functor + ' ').join(args) + ')'

    def __eq__(self, other):
        """x and y are equal iff their functors and args are equal."""
        return (isinstance(other, Literal)
                and self.functor == other.functor
                and self.args == other.args)

    def __hash__(self):
        "Need a hash method so Literals can live in dicts."
        return hash(self.functor) ^ hash(tuple(self.args))

# Parse Literal
def parse_literal(content):
    literal = None
    # Se for string, quebra ela em literais
    if isinstance(content, str):
        regex_literal = '^\s*([~])?(\w*)[\(\s*]?([\w,\s]*)[\s*\)]?$'
        literal_content = re.findall(regex_literal, content)
        if literal_content:
            literal_content = literal_content.pop()
            # Negation
            if literal_content[0].strip():
                literal = Literal(literal_content[0].strip())
            # Functor
            functor = Literal(literal_content[1].strip())
            if literal:
                literal.args = {functor}
            else:
                literal = functor
            # Arguments
            arguments = []
            arguments_content = literal_content[2].strip()
            if arguments_content:
                arguments_content = re.split(',', arguments_content)          
                for argument_content in arguments_content:
                    argument_content = argument_content.strip()
                    arguments.append(Literal(argument_content))
                functor.args = arguments

    return literal

def unify(t1, t2, theta):
    if theta is None:
        return None
    elif t1 == t2:
        return theta
    elif is_variable(t1):
        return unify_var(t1, t2, theta)
    elif is_variable(t2):
        return unify_var(t2, t1, theta)
    elif isinstance(t1, Literal) and isinstance(t2, Literal):
        return unify(t1.args, t2.args, unify(t1.functor, t2.functor, theta))
    elif isinstance(t1, str) or isinstance(t2, str):
        return None
    elif is_sequence(t1) and is_sequence(t2) and len(t1) == len(t2):
        if not t1:
            return theta
        return unify(t1[1:], t2[1:], unify(t1[0], t2[0], theta))
    else:
        return None

def substitute(substitution, literal):
    if isinstance(literal, list):
        return [substitute(substitution, item) for item in literal]
    elif isinstance(literal, tuple):
        return tuple([substitute(substitution, item) for item in literal])
    elif not isinstance(literal, Literal):
        return literal
    elif is_var_symbol(literal.functor):
        return substitution.get(literal, literal)
    else:
        return Literal(literal.functor, *[substitute(substitution, arg) for arg in literal.args])

def is_sequence(var):
    "Is var a sequence? We say it is if it has a __getitem__ method."
    return hasattr(var, '__getitem__')

def is_number(var):
    "Is var a number? We say it is if it has a __int__ method."
    return hasattr(var, '__int__')

def is_symbol(var):
    "A string var is a symbol if it starts with an alphabetic char."
    return isinstance(var, str) and var[0].isalpha()

def is_var_symbol(var):
    "A logic variable symbol is an initial-uppercase string."
    return is_symbol(var) and var[0].isupper()

def is_variable(var):
    "A variable is an Literal with no args and a uppercase symbol as the functor."
    return isinstance(var, Literal) and not var.args and is_var_symbol(var.functor)

def unify_var(var, term, theta):
    if var in theta:
        return unify(theta[var], term, theta)
    elif occur_check(var, term):
        return None
    else:
        return extend(theta, var, term)

def occur_check(var, term):
    if var == term:
        return True
    elif isinstance(term, Literal):
        return var.functor == term.functor or occur_check(var, term.args)
    elif not isinstance(term, str) and is_sequence(term):
        for xi in term:
            if occur_check(var, xi): return True
    return False

def extend(theta, var, val):
    new_theta = theta.copy()
    new_theta[var] = val
    return new_theta