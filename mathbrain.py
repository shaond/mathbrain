#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asciimathml as am

from xml.etree.ElementTree import tostring
from jinja2 import Environment, PackageLoader

def qInequalities_template():
    '''Solve inequalities.'''
    env = Environment(loader=PackageLoader('mathbrain', 'templates'))
    template = env.get_template('template1.html')
    from random import choice, randint
    from math import pow
    from sympy import solve, Poly, Eq, Function, exp
    from sympy.abc import x
    

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
    q, a = qExponentialSameBase_template()
    question.append(q)
    answer.append(a)
    print question
    print answer
    

if __name__ == '__main__':
    main()
