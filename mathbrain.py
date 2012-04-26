#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asciimathml as am

from xml.etree.ElementTree import tostring
from jinja2 import Environment, PackageLoader
from sympy import solve, Poly, Eq, Function, exp, Le, Lt, Ge, Gt
from sympy import pi, cse, sqrt, simplify, diff, ln
from sympy.mpmath import nthroot, root
from sympy.printing import mathml
from sympy.abc import x
from random import choice, randint
from math import pow, log10, floor

def qGrpDifferentiation_template():
    '''Group Differentiation  e.g. diff x^2*e^x'''
    #TODO: Need to make this more random selection
    type_diff1 = randint(0,3) #normal,exp,trig,log
    type_diff2 = randint(0,3) #normal,exp,trig,log
    first_val = randint(-100,100)
    second_val = randint(-100,100)
    question = 'Differentiate ' + tostring(am.parse('ln((%sx%s))' 
                                                    % (first_val, second_val))) 
    question += ' with respect to ' + tostring(am.parse('x'))

    steps = []
    diff_inside = diff(first_val*x+second_val)
    steps.append('Differentiate %s normally' % tostring(am.parse('%sx%s' %
                                               (first_val, second_val))))
    steps.append('This will give %s which goes as numerator' % str(diff_inside))
    steps.append('%s goes as denominator' % tostring(am.parse('%sx%s' %
                                               (first_val, second_val))))
    answer = []
    answer.append(steps)
    answer.append(tostring(am.parse(str(diff(ln(first_val*x+second_val))))))

    return question, answer

def qExpDifferentiation_template():
    '''Differeniate exponential e.g. diff e^(2x^3+2)'''
    rand_power = randint(2,100) #Can't do -ve as this is calculated differently
    front_num = randint(-100,100)
    while front_num == 0:
        front_num = randint(-100,100)
    end_num = randint(-100,100)
    while front_num == 0:
        end_num = randint(-100,100)
    if end_num < 0:
        question = 'Differentiate ' + tostring(am.parse('e^(%sx^(%s)%s)' 
                                                        % (front_num,
                                                           rand_power,
                                                           end_num)))
    else:
        question = 'Differentiate ' + tostring(am.parse('e^(%sx^(%s)+%s)' 
                                                        % (front_num,
                                                           rand_power,
                                                           end_num)))
    question += ' with respect to ' + tostring(am.parse('x'))

    steps = []
    diff_top = diff(front_num*x**(rand_power)+end_num)
    if end_num < 0:
        steps.append('Differentiate %s normally' % tostring(am.parse('%sx^(%s)%s' 
                                                                     % (front_num, 
                                                                        rand_power,
                                                                        end_num))))
    else:
        steps.append('Differentiate %s normally' % tostring(am.parse('%sx^(%s)+%s' 
                                                                     % (front_num, 
                                                                        rand_power,
                                                                        end_num))))
    steps.append('This will give %s which goes at front of original question' 
                 % tostring(am.parse(str(diff_top).replace("**","^"))))
    answer = []
    answer.append(steps)
    diff_val = diff(exp(front_num*x**(rand_power)+end_num))
    answer.append(tostring(am.parse(str(diff_val).replace("**","^").
                                   replace("exp", "e^"))))

    return question, answer

def qLogDifferentiation_template():
    '''Differeniate log(e) e.g. diff ln(5*x+2)'''
    first_val = randint(-100,100)
    second_val = randint(-100,100)
    if second_val < 0:
        question = 'Differentiate ' + tostring(am.parse('ln((%sx%s))' 
                                                        % (first_val, 
                                                           second_val))) 
    else:
        question = 'Differentiate ' + tostring(am.parse('ln((%sx+%s))' 
                                                        % (first_val, 
                                                           second_val))) 
    question += ' with respect to ' + tostring(am.parse('x'))

    steps = []
    # TODO there's a bug here.
    # ValueErorr: specify differentiation variables to differentiate 86
    diff_inside = diff(first_val*x+second_val)
    steps.append('Differentiate %s normally' % tostring(am.parse('%sx%s' %
                                               (first_val, second_val))))
    steps.append('This will give %s which goes as numerator' % str(diff_inside))
    steps.append('%s goes as denominator' % tostring(am.parse('%sx%s' %
                                               (first_val, second_val))))
    answer = []
    answer.append(steps)
    answer.append(tostring(am.parse(str(diff(ln(first_val*x+second_val))))))

    return question, answer

def qSimplifyBinomial_template():
    '''Simplify Binomial e.g. Simplify n^2-25/n-5.'''
    base = choice([2,3,5,7])
    pow_base = pow(base, 2)
    numerator = x**2-int(pow_base)
    denominator = x-base
    question = 'Simplify ' + tostring(am.parse('(x^2-%s)/(x-%s)' %
                                               (int(pow_base), base)))

    steps = []
    steps.append('Covert numerator to binomial to match denominator.')
    binomial = tostring(am.parse('x^2-%s' % (int(pow_base))))
    expanded_binomial = tostring(am.parse('(x-%s)(x+%s)' % (base,base)))
    steps.append('As '+ binomial + ' is the same as ' + expanded_binomial)
    steps.append('Therefore ' + tostring(am.parse('((x-%s)(x+%s))/(x-%s)' %
                                                  (base,base,base))))
    steps.append('Cancel '+ tostring(am.parse('(x-%s)' %(base))) + 
                 ' from denominator and numerator')
    answer = []
    answer.append(steps)
    answer.append(tostring(am.parse(str(simplify(numerator/denominator)))))

    return question, answer

def qSignificantFigures_template():
    '''Significant figures. e.g. Evaluate cuberoot(651/3) to 5 sig fig.'''
    sig_fig = randint(2,5)
    root_val = randint(2,5)
    numerator = randint(1,1000)
    denom = randint(1,1000)
    val = 'root%s(%s/(%s*pi))' % (root_val, numerator, denom)
    question = 'Evaluate ' +  tostring(am.parse(val)) + ' to %s' % (sig_fig)
    question += ' Significant Figures.'

    steps = []
    inside_root = (numerator/(denom*pi)).evalf() 
    val = root(inside_root, root_val)
    steps.append('This has to be done with a calculator.')
    steps.append('Do the inside calucation first: ' + 
                 tostring(am.parse('%s/(%s*pi)'%(numerator,denom))) + tostring(am.parse('*'))
                 + str(am.parse('pi')))
    steps.append('This should give ' + tostring(am.parse(str(inside_root))))
    steps.append('Then use 1/y key on calculator and press ' + str(root_val))
    steps.append('Then get the value to %s significant figures.' % sig_fig)
    answer = []
    answer.append(steps)
    answer.append(round(val, sig_fig-int(floor(log10(val)))-1))

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
    answer.append(str(solve(question, x)))

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

    # TODO there's a bug here.
    # TypeError: object of type 'bool' has no len()
    if len(solve(Eq(lspow, rs))) > 1:
        answer.append(tostring(am.parse('x = %s' % solve(Eq(lspow, rs))[0])))
    else:
        answer.append(tostring(am.parse('x = %s' % solve(Eq(lspow, rs))[0])))

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

    q, a = qExpDifferentiation_template()
    questions.append(q)
    answers.append(a)

    q, a = qLogDifferentiation_template()
    questions.append(q)
    answers.append(a)

    q, a = qSimplifyBinomial_template()
    questions.append(q)
    answers.append(a)

    q, a = qSignificantFigures_template()
    questions.append(q)
    answers.append(a)

    q, a = qExponentialSameBase_template()
    questions.append(q)
    answers.append(a)

    q, a = qInequalities_template()
    questions.append(q)
    answers.append(a)

    render_question_paper(questions, answers)

    

if __name__ == '__main__':
    main()
