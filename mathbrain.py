#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asciimathml as am

from xml.etree.ElementTree import tostring
from jinja2 import Environment, PackageLoader
from sympy import solve, Poly, Eq, Function, exp, Le, Lt, Ge, Gt
from sympy.printing import mathml
from sympy.abc import x
from random import choice, randint
from math import pow

def qSignificantFigures_template():
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


def qInequalities_template():
    '''Solve inequalities. e.g. 2-3x <= 8.'''
    leftside_section1 = randint(-100,100)
    leftside_section2 = randint(-100,100)
    left_side = leftside_section1 + leftside_section2
    right_side = randint(-100,100)
    equality_type = randint(0,3) #<, <=, >, >=
    question = None 
    question_str = "Solve : "
    if equality_type == 0:
        question = Lt(leftside_section1 + leftside_section2*x, right_side)
    elif equality_type == 1:
        question = Le(leftside_section1 + leftside_section2*x, right_side)
    elif equality_type == 2:
        question = Gt(leftside_section1 + leftside_section2*x, right_side)
    elif equality_type == 3:
        question = Ge(leftside_section1 + leftside_section2*x, right_side)
    question_str += tostring(am.parse(str(question)))

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
    answer.append(mathml(solve(question, x)))

    return question_str, answer

def qExponentialSameBase_template():
    '''Solves the same base e.g. 2^(2x+1) = 32.'''
    base = choice([2,3,5,7])
    pow_rs = randint(3,6)
    rs = int(pow(base,pow_rs))
    lspow = randint(-10,10)*x+randint(-100,100)
    question = tostring(am.parse('%s^(%s) = %s' % (base, lspow, rs)))

    steps = []
    steps.append('Covert right side to be same base as left side - left side' \
                  ' is base ' + str(base))
    steps.append('Right side is now: ' + tostring(am.parse('%s^(%s)' % 
                                                           (base, rs))))
    steps.append('Therefore solve ' + tostring(am.parse('%s%s%s' %
                                                        (lspow,'=',rs)))) 
    answer = []
    answer.append(steps)
    answer.append(solve(Eq(lspow, rs))[0])

    return question, answer


def render_question_paper(q, a):
    '''Generates the final question paper & answer sheet.'''
    env = Environment(loader=PackageLoader('mathbrain', 'templates'))
    template_questions = env.get_template('template_questions.html')
    template_answers = env.get_template('template_answers.html')
    print template_questions.render(questions=q)
    # print template_answers.render(answers=a)


def main():
    '''Generating a template'''

    questions = []
    answers = []

    q, a = qExponentialSameBase_template()
    questions.append(q)
    answers.append(a)

    q, a = qInequalities_template()
    questions.append(q)
    answers.append(a)

    render_question_paper(questions, answers)

    

if __name__ == '__main__':
    main()
