#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asciimathml as am

from xml.etree.ElementTree import tostring
from jinja2 import Environment, PackageLoader
from sympy import solve, Poly, Eq, Function, exp, Le, Lt, Ge, Gt
from sympy import pi, cse, sqrt, simplify, diff, ln, sin, cos, tan, expand
from sympy import radsimp, factor, together, Symbol, integrate, real_roots
from sympy.mpmath import nthroot, root, limit
from sympy.printing import mathml
from sympy.abc import x, y, u, t
from random import choice, randint
from math import pow, log10, floor
import re

def qSeconDiffInvolvingInverseTan_template():
    '''If y = tan^-1(x^2), find d^2y/dx^2.'''

    x_pow = randint(2,5)
    question = "If " + tostring(am.parse("y=ta"))
    question += tostring(am.parse("n^(-1)(x^%s)," % x_pow))
    question += " find " + tostring(am.parse("(d^2y)/(dx^2)."))

    steps = []
    first_diff = (x_pow*x)/(1+x**x_pow)
    second_diff = diff(first_diff)
    second_diff_str = str(second_diff).replace("**", "^")
    val_regex = re.compile("/")
    val2_regex = re.compile("\+")
    second_diff_str_mod = val_regex.split(second_diff_str)
    second_diff_str_mod2 = val2_regex.split(second_diff_str_mod[1])
    steps.append(tostring(am.parse(" (dy)/(dx)= %s" % 
                                   str(first_diff).replace("**", "^"))))

    answer = []
    answer.append(steps)
    answer.append(tostring(am.parse(" (d^2y)/(dx^2)= (%s)/(%s+%s)+(%s)/(%s)" %
                                    (second_diff_str_mod[0],
                                     second_diff_str_mod2[0],
                                     second_diff_str_mod2[1],
                                     second_diff_str_mod2[2],
                                     second_diff_str_mod[2]))))

    return question, answer

def qDivInterval_template():
    '''Division of Point e.g. The Point P divides the interval joining 
    A(-1, 2) to B(9,3) internally in the ratio 4:1. 
    Find the coordinates of P.'''
    #http://www.teacherschoice.com.au/Maths_Library/Analytical%20Geometry/AnalGeom_3.htm

    xa = randint(-10,10)
    xb = randint(-10,10)
    ya = randint(-10,10)
    yb = randint(-10,10)
    k1 = randint(1,10)
    k2 = randint(1,20)
    while yb == ya:
        yb = randint(-10,10)
    while k1 == k2:
        k2 = randint(1,20)
    question = "The Point " + tostring(am.parse("P"))
    question += " divides the interval joining " + tostring(am.parse("A(%s,%s)"
                                                                    %(xa, ya)))
    question += " to " +  tostring(am.parse("B(%s,%s)" %(xb, yb)))
    question += " internally in the ratio " +  tostring(am.parse("%s:%s" 
                                                                 %(k1, k2)))

    steps = []
    xp = simplify((k1*x+k2*u)/(k1 + k2)).subs(x,xb).subs(u,xa)
    yp = simplify((k1*y+k2*t)/(k1 + k2)).subs(y,yb).subs(t,ya)
    steps.append(tostring(am.parse("x_p = ((%s)*(%s) + (%s)*(%s))/(%s+%s)" 
                                   % (k1, xb, k2, xa, k1, k2))))
    steps.append(tostring(am.parse("y_p = ((%s)*(%s) + (%s)*(%s))/(%s+%s)" 
                                   % (k1, yb, k2, ya, k1, k2))))
    steps.append("Refer to http://www.teacherschoice.com.au/Maths_Library/Analytical%20Geometry/AnalGeom_3.htm")

    answer = []
    answer.append(steps)
    answer.append(tostring(am.parse("P(%s,%s)" %(xp, yp))))

    return question, answer

def qSimpleLimits_template():
    '''Limits e.g. lim h->0 sin(h/2)/h'''
    #ans_limit = limit(lambda x: (sin(x/5))/x, 0)

    denominator = randint(2,10)
    question = "Determine " 
    question_str = tostring(am.parse("lim_(x->0)(sin(x/%s))/x" % denominator)) 
    question += question_str

    steps = []
    working_out_eqn = tostring(am.parse("=lim_(x->0)1/%s*(sin(x/%s))/(x/%s)" %
                                        (denominator, denominator,
                                         denominator))) 
    steps.append(question_str + working_out_eqn)

    answer = []
    answer.append(steps)
    answer.append(tostring(am.parse("1/%s" % denominator)))

    return question, answer

def qSimpleTSubstitutionCos_template():
    '''t substitution
    e.g. If t = tan x/2, express as simply as possible in terms of t, (1-cosx)/(1+cosx)'''
    
    front_num = randint(-3,3)
    while front_num == 0: 
        front_num = randint(-3,3)

    denom_positive = randint(0, 1)

    question = "If " + tostring(am.parse("t=tan(x/2)")) 
    question += " express as simply as possible in terms of " + \
            tostring(am.parse("t,"))
    question_eqn = None
    question_eqn_str = None
    eqn_sub_top = None
    if denom_positive  == 1: 
        eqn_sub_top = (front_num+cos(x))
        eqn_sub_bott = (front_num-cos(x))
        question_eqn = (eqn_sub_top)/(eqn_sub_bott)
        question_eqn_str = tostring(am.parse("(%s+cos(x))/(%s-cos(x))" %
                                             (front_num, front_num)))
    else: 
        eqn_sub_top = (front_num-cos(x))
        eqn_sub_bott = (front_num+cos(x))
        question_eqn = (eqn_sub_top)/(eqn_sub_bott)
        question_eqn_str = tostring(am.parse("(%s-cos(x))/(%s+cos(x))" %
                                             (front_num, front_num)))

    question += " " + question_eqn_str

    u = (1-t**2)/(1+t**2)
    eqn_sub = question_eqn.subs(cos(x), u)
    eqn_sub_str = str(eqn_sub).replace("**","^")
    eqn_top = simplify(expand(eqn_sub_top.subs(cos(x),u)))
    eqn_top_str = str(eqn_top).replace("**","^")
    eqn_bott = simplify(expand(eqn_sub_bott.subs(cos(x),u)))
    eqn_bott_str = str(eqn_bott).replace("**","^")
    eqn_simplified = simplify(eqn_sub)
    eqn_simplified_str = str(eqn_simplified).replace("**","^")

    steps = []
    steps.append(question_eqn_str + tostring(am.parse("=%s" % (eqn_sub_str))))
    steps.append(tostring(am.parse("=(%s)/(%s)" % (eqn_top_str, eqn_bott_str))))

    answer = []
    answer.append(steps)
    answer.append(tostring(am.parse("%s" % eqn_simplified_str)))

    return question, answer

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
    integ_eqn = integrate(eqn_expanded)
    integ_eqn_str = str(integ_eqn).replace("**","^")
    min_sub = integ_eqn.subs(x, x_min)
    max_sub = integ_eqn.subs(x, x_max)
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
                                   (diff_du, integ_eqn_str, x_min, x_max)))) 
    steps.append(tostring(am.parse("= %s[(%s)-(%s)]" % 
                                   (diff_du, max_sub_str, min_sub_str)))) 

    answer = []

    answer.append(steps)
    answer.append(tostring(am.parse("%s" % (diff_du*(max_sub-min_sub))))) 

    return question, answer

def render_question_paper(q, a):
    '''Generates the final question paper & answer sheet.'''
    env = Environment(loader=PackageLoader('mathbrain', 'templates'))
    template_questions = env.get_template('template_questions_ext.html')
    template_answers = env.get_template('template_answers_ext.html')
    
    try:
        questions_html = open('questions_ext.html', 'w')
        answers_html = open('answers_ext.html', 'w')

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

    #Second iteration

    #First iteration
    q, a = qSeconDiffInvolvingInverseTan_template()
    questions.append(q)
    answers.append(a)

    q, a = qDivInterval_template()
    questions.append(q)
    answers.append(a)

    q, a = qIntegrationBySub_template()
    questions.append(q)
    answers.append(a)

    q, a = qSimpleTSubstitutionCos_template()
    questions.append(q)
    answers.append(a)

    q, a = qSimpleLimits_template()
    questions.append(q)
    answers.append(a)

    render_question_paper(questions, answers)
    

if __name__ == '__main__':
    main()
