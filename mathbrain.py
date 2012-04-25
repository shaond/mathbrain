#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asciimathml as am

from xml.etree.ElementTree import tostring
from jinja2 import Environment, PackageLoader
from sympy import solve, Poly, Eq, Function, exp, Le, Lt, Ge, Gt
from sympy import pi, cse, sqrt, simplify
from sympy.mpmath import nthroot, root
from sympy.printing import mathml
from sympy.abc import x
from random import choice, randint
from math import pow, log10, floor

def qSimplifyBinomial_template():
    '''Simplify Binomial e.g. Simplify n^2-25/n-5.'''
    base = choice([2,3,5,7])
    pow_base = randint(3,6)
    numerator = x**2-pow_base
    denominator = x-pow_base
    bin_equation = exp((numerator)/(denominator))
    question = 'Simplify' + tostring(am.parse('x^2-%s/x-%s' % (pow_base, base)))

    steps = []
    steps.append('Covert numerator to binomial to match denominator.')
    steps.append('As '+ str(base))
    answer = []
    answer.append(steps)
    answer.append(simplify(bin_equation))

    return question, answer

def qSignificantFigures_template():
    '''Significant figures. e.g. Evaluate cuberoot(651/3) to 5 sig fig.'''
    sig_fig = randint(2,5)
    root_val = randint(2,5)
    numerator = randint(1,1000)
    denom = randint(1,1000)
    #val = cse(sqrt((numerator/denom)))
    #print val
    question = 'Evaluate ' +  tostring(am.parse(val)) + ' to ' 
    question += str(sig_fig) + ' Significant Figures.'
    #question = 'Evaluate ' +  mathml(nthroot(numerator/(denom*pi), root_val)) +\
    #           'to ' + str(sig_fig) + 'significant figures.'

    steps = []
    steps.append('This has to be done with a calculator.')
    steps.append('Do the inside calucation first: ' + str(numerator) +
                 tostring(am.parse('/')) + str(denom) + tostring(am.parse('*'))
                 + str(amp.parse(pi)))
    steps.append('This should give: ' + str(numerator/(denom*pi)))
    steps.append('Then use 1/y key on calculator and press :' + str(root_val))
    answer = []
    answer.append(steps)
    answer.append(round(val, sig-int(floor(log10(val)))-1))

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

    #q, a = qSignificantFigures_template()
    #questions.append(q)
    #answers.append(a)

    q, a = qExponentialSameBase_template()
    questions.append(q)
    answers.append(a)

    q, a = qInequalities_template()
    questions.append(q)
    answers.append(a)

    render_question_paper(questions, answers)

    

if __name__ == '__main__':
    main()
