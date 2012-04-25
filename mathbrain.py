#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asciimathml as am

from xml.etree.ElementTree import tostring
from jinja2 import Environment, PackageLoader
from sympy import solve, Poly, Eq, Function, exp, Le, Lt, Ge, Gt
from sympy.abc import x
from random import choice, randint
from math import pow

def qInequalities_template():
    '''Solve inequalities. e.g. 2-3x <= 8.'''
    leftside_section1 = randint(-100,100)
    leftside_section2 = randint(-100,100)
    left_side = leftside_section1 + leftside_section2
    right_side = randint(-100,100)
    equality_type = randint(0,3) #<, <=, >, >=
    question = None 
    if equality_type == 0:
        question = Lt(leftside_section1 + leftside_section2*x, right_side)
    elif equality_type == 1:
        question = Le(leftside_section1 + leftside_section2*x, right_side)
    elif equality_type == 2:
        question = Gt(leftside_section1 + leftside_section2*x, right_side)
    elif equality_type == 3:
        question = Ge(leftside_section1 + leftside_section2*x, right_side)
    steps = []
    if leftside_section1 < 0:
        steps.append('Move by +' + str(leftside_section1*-1) + ' to both ' \
                     +'sides')
    else:
        steps.append('Move by -' + str(leftside_section1) + ' to both ' \
                     +'sides')
    steps.append('Divide left and right side by ' + str(leftside_section2))
    answer = []
    answer.append(steps)
    answer.append(solve(question, x))

    return question, answer

def qExponentialSameBase_template():
    '''Solves the same base e.g. 2^(2x+1) = 32.'''
    env = Environment(loader=PackageLoader('mathbrain', 'templates'))
    template = env.get_template('template.html')
    from random import choice, randint
    from math import pow
    base = choice([2,3,5,7])
    pow_rs = randint(3,6)
    rs = int(pow(base,pow_rs))
    lspow = '2x+1'
    print template.render(leftside=tostring(am.parse('%s^(%s)' % (base, lspow))),
                          equality=tostring(am.parse('=')), 
                          rightside=tostring(am.parse('%s' % rs)),
                          lspow=tostring(am.parse(lspow)),
                          samebase_rightside=tostring(am.parse('%s^(%s)' %
                              (base,pow_rs))),
                          rs_pow = tostring(am.parse('%s' % pow_rs)))
    return question, answer


def main():
    '''Generating a template'''
    question = []
    answer = []
    #q, a = qExponentialSameBase_template()
    #question.append(q)
    #answer.append(a)
    q, a = qInequalities_template()
    question.append(q)
    answer.append(a)
    print question
    print answer
    

if __name__ == '__main__':
    main()
