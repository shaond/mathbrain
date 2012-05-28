#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asciimathml as am

from xml.etree.ElementTree import tostring
from jinja2 import Environment, PackageLoader
from sympy import solve, Poly, Eq, Function, exp, Le, Lt, Ge, Gt
from sympy import pi, cse, sqrt, simplify, diff, ln, sin, cos, tan, expand
from sympy import radsimp, factor, together, Symbol, integrate, real_roots
from sympy.mpmath import nthroot, root
from sympy.printing import mathml
from sympy.abc import x, y, u
from random import choice, randint
from math import pow, log10, floor
import re

def qIntegrationBySub_template():
    '''Integration by substitution
    e.g. Use the subsitution x=1-2u to evaluate Integral(2u(1-2u)^4) du'''
    u_front = randint(2, 10)
    front_num = randint(-100,100)
    while front_num == 0: 
        front_num = randint(-100,100)

    u_max = randint(11, 20)
    u_min = randint(1, 10)
    pow_val = randint(2, 5)

    question = "Use the substitution " 
    subsition_str = None
    if u_front > 0: 
        substitution_str = tostring(am.parse("x=%s+%su" % (front_num,u_front)))
    else: 
        substitution_str = tostring(am.parse("x=%s%su" % (front_num,u_front)))

    question += substitution_str
    question += " to evaluate " 
    question_eqn_str = None
    if u_front > 0: 
        question_eqn_str = tostring(am.parse("int_(%s)^(%s)%su(%s+%su)^%s du" %
                                             (u_min, u_max, u_front,
                                              front_num, u_front, pow_val))) 
    else: 
        question_eqn_str = tostring(am.parse("int_(%s)^(%s)%su(%s%su)^%s du" %
                                             (u_min, u_max, u_front,
                                              front_num, u_front, pow_val))) 
    question += question_eqn_str

    #Needed states 
    diff_dx = diff(front_num+u_front*u)
    diff_du = 1/diff_dx
    x_min = front_num+u_front*u_min
    x_max = front_num+u_front*u_max
    x_front = x-front_num
    eqn_expanded = ((x-front_num)*(x**pow_val)).expand(basic=True) 
    eqn_expanded_str = str(eqn_expanded).replace("**","^")
    min_sub = eqn_expanded.subs(x, x_min)
    max_sub = eqn_expanded.subs(x, x_max)
    min_sub_str = str(min_sub).replace("**","^")
    max_sub_str = str(max_sub).replace("**","^")

    steps = []
    steps.append(tostring(am.parse("u=%s, x=%s" % (u_min, x_min)))) 
    steps.append(tostring(am.parse("u=%s, x=%s" % (u_max, x_max)))) 
    steps.append(tostring(am.parse("(dx)/(du) = %s, (du)/(dx) = %s" % 
                                   (diff_dx, diff_du)))) 
    if u_front > 0: 
        steps.append(tostring(am.parse("int_(%s)^(%s)%su(%s+%su)^%s du = " \
                                       "int_(%s)^(%s)(%s)(x)^%s(%s) dx" % 
                                       (u_min, u_max, 
                                        u_front, front_num, u_front, pow_val,
                                        x_min, x_max, x_front, 
                                        pow_val, diff_du)))) 
    else: 
        steps.append(tostring(am.parse("int_(%s)^(%s)%su(%s%su)^%s du = " \
                                       "int_(%s)^(%s)(%s)(x)^%s(%s) dx" % 
                                       (u_min, u_max, 
                                        u_front, front_num, u_front, pow_val,
                                        x_min, x_max, x_front, 
                                        pow_val, diff_du)))) 
    steps.append(tostring(am.parse("= %sint_(%s)^(%s)(%s) dx" % 
                                   (diff_du, x_min, x_max, eqn_expanded_str)))) 
    steps.append(tostring(am.parse("= %s[%s]_(%s)^(%s)" % 
                                   (diff_du, eqn_expanded_str, x_min, x_max)))) 
    steps.append(tostring(am.parse("= %s[(%s)-(%s)]" % 
                                   (diff_du, max_sub_str, min_sub_str)))) 

    answer = []

    answer.append(steps)
    answer.append(tostring(am.parse("%s" % (diff_du*(max_sub-min_sub))))) 

    return question, answer

def render_question_paper(q, a):
    '''Generates the final question paper & answer sheet.'''
    env = Environment(loader=PackageLoader('mathbrain', 'templates'))
    template_questions = env.get_template('template_questions.html')
    template_answers = env.get_template('template_answers.html')
    
    try:
        questions_html = open('questions.html', 'w')
        answers_html = open('answers.html', 'w')

        # Generate our question paper.
        questions_html.write(template_questions.render(questions=q))

        # Extract the solution and all working our steps.
        steps = a[0]
        solution = a[1]
        answers_html.write(template_answers.render(answers=a))

        # Close open files.
        questions_html.close()
        answers_html.close()
    except IOError as (errno, strerr):
        sys.exit("IOError (%d): %s".format(errno, strerr))


def main():
    '''Generating a template'''

    questions = []
    answers = []

    q, a = qIntegrationBySub_template()
    questions.append(q)
    answers.append(a)

    q, a = qIntegrationBySub_template()
    questions.append(q)
    answers.append(a)

    render_question_paper(questions, answers)
    

if __name__ == '__main__':
    main()
