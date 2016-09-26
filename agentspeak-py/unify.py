# Fonte: http://aima.cs.berkeley.edu/python/logic.html

import copy

def is_symbol(s):
    "A string s is a symbol if it starts with an alphabetic char."
    return isinstance(s, str) and s[0].isalpha()

def is_var_symbol(s):
    "A logic variable symbol is an initial-lowercase string."
    return is_symbol(s) and s[0].islower()

def is_variable(s):
    return is_var_symbol(s)

def extend(theta, variable, term):
    new_theta = copy.copy(theta)
    new_theta[variable] = term
    return new_theta

def occur_check(variable, term):
    if variable == term:
        return True
    # elif is_structure(term):
    #     return term.head == variable.head or occur_check(variable, term.arguments)
    return False

def unify_variable(variable, term, theta):
    print 'variable: %s' % variable
    print 'term: %s' % term
    print 'theta: %s' %theta
    if variable in theta:
        return unify(theta[variable], term, theta)
    elif occur_check(variable, term):
        return None
    else:
        return extend(theta, variable, term)


def unify(t1, t2, theta):
    # print 't1: %s' % t1
    # print 't2: %s' % t2
    if theta == None:
        return None
    elif t1 == t2:
        return theta
    elif is_variable(t1):
        return unify_variable(t1, t2, theta)
    elif is_variable(t2):
        return unify_variable(t2, t1, theta)
    # elif is_structure(t1) and is_structure(t2) and (t1.head == t2.head):
    #     # Unifica recursivamente quando o argumento for uma estrutura
    #     new_theta = theta
    #     if len(t1.arguments) == len(t2.arguments):
    #         for i in range(len(t1.arguments)):
    #             new_theta = unify(t1.arguments[i], t2.arguments[i], new_theta)
    #         return new_theta
    #     else:
    #         return None
    else:
        return None


if __name__ == '__main__':
    theta = {}
    event = '!start'
    beliefs = ['!start', 'a(p)', '~a(p)']

    unify_beliefs = [unify(event, belief, theta) for belief in beliefs]

    print unify_beliefs