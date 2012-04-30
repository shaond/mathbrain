#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asciimathml as am

from xml.etree.ElementTree import tostring
from jinja2 import Environment, PackageLoader
from sympy import solve, Poly, Eq, Function, exp, Le, Lt, Ge, Gt
from sympy import pi, cse, sqrt, simplify, diff, ln, sin, cos, tan
from sympy import radsimp, factor, together, Symbol, integrate
from sympy.mpmath import nthroot, root
from sympy.printing import mathml
from sympy.abc import x
from random import choice, randint
from math import pow, log10, floor
import re

def qIntegrationNegativePower_template():
    '''Integration involving a negative power e.g. 1/x^2.'''
    '''Reason why this is asked is because students mistake this for ln()'''
    pow_val = randint(2,9)
    front_num = randint(-100,100)
    #Note we remove the front number if -1 or 1 for time being to avoid logic
    while front_num <= 1 and front_num >=-1: 
        front_num = randint(-100,100)
    question = "Find " + tostring(am.parse('int1/(%sx^%s)dx'% (str(front_num),
                                                               str(pow_val))))

    steps = []
    num_log_diff = diff(front_num*x**pow_val)
    true_log_integrate = tostring(am.parse('int(%s)/(%sx^%s)dx'%
                                           (str(num_log_diff).
                                            replace("**", "^"),
                                            str(front_num),
                                            str(pow_val)))) 
    steps.append("This is not a logarithmic integration.")
    steps.append("The reason is that the diff of the bottom x value should " + \
                 "go on top which is the premise behind a logarithmic " + \
                 "integration but the question does not show this. If you " + \
                 "see " + true_log_integrate + " then it is.")
    group_integrate = tostring(am.parse('int(%sx)^-%sdx'% (str(front_num),
                                                           str(pow_val)))) 
    steps.append("Integrate this normally as: " + group_integrate + \
                 " which is the same as " + \
                 tostring(am.parse('int1/(%sx^%s)dx' % (str(front_num),
                                                        str(pow_val)))))
    steps.append("Integrating this will be: [1 / (diff of " +
                 tostring(am.parse("%sx*-%s" % (str(front_num),
                                                str(pow_val)))) + 
                 ")]" + tostring(am.parse("*(%sx)^(-%s+1)" % (str(front_num),
                                                              str(pow_val)))))

    answer = []
    answer.append(steps)
    ans = integrate(1/(front_num*x**pow_val))
    answer.append(tostring(am.parse(str(ans).replace("**","^"))))

    return question, answer

def qSimpleBatchProbability_template():
    '''Simple Batch Probability problem.'''
    num_items = randint(100, 20000)
    defective_prob = float(randint(1,100))/1000 #Want it to be 0.001 accuracy
    question = "A batch of " + str(num_items) + " items is examained. " + \
            "The probability of an item in this batch being defective is " + \
            str(defective_prob)
    question += ". How many items from this batch are defective?"

    steps = []
    prob_eqn = tostring(am.parse("Pr(E)=(n(E))/(n(S))"))
    prob_word_eqn = tostring(am.parse("Probability(Event)=(" + \
                                      "# of Events)/(" + \
                                      "# of Sample Space)"))
    steps.append("The probability of defectiveness is governed by the"+ \
                 "following equation: " + prob_word_eqn + " known as: " + \
                 prob_eqn)
    steps.append("As we are given " + tostring(am.parse("Pr(E)=%s" %
                                                        str(defective_prob))) +\
                 " which is the defective probability ")
    steps.append("Also we are given " + tostring(am.parse("n(s)=%s" %
                                                        str(num_items))) + \
                 " which is the number of items in the batch (sample space) ")
    steps.append("Therefore we need to find " + tostring(am.parse("n(E)=Pr" + \
                                                                  "(E)*n(s)")))
    steps.append("This gives " + tostring(am.parse("n(E)=%s*%s" %
                                                   (str(defective_prob),
                                                    str(num_items))))) 
    answer = []
    answer.append(steps)
    ans = float(num_items)*defective_prob
    answer.append(tostring(am.parse(str(ans))))

    return question, answer

def qRationaliseDenominator_template():
    '''Ratoinalise Denominator e.g. Rataionlise 4/(root(4)-root(5))'''
    numerator = choice([2,3,5,6,7,8,10,11,20,32])
    first_root = choice([2,3,5,6,7,8,10,11,20,32])
    second_root = choice([2,3,5,6,7,8,10,11,20,32])
    #first_root = randint(2,20)
    #second_root = randint(2,20)
    while second_root == first_root:
        second_root = choice([2,4,6,8,16,20])
    type_denom = randint(0,1) #Either + or -
    type_val = None
    opp_val = None
    if not type_denom:
        type_val, opp_val = "-", "+"
    else:
        type_val, opp_val = "+", "-"
    question_print = tostring(am.parse('%s/(sqrt%s%ssqrt%s)' 
                                       % (str(numerator),
                                          str(first_root),
                                          str(type_val),
                                          str(second_root))))

    question = 'Rationalise the denominator of ' + question_print
    question += '. Give your answer in the simplest form.'

    steps = []
    step_print = tostring(am.parse('sqrt%s%ssqrt%s' % (first_root,
                                                       opp_val,
                                                       second_root)))
    step_multiply = tostring(am.parse('(sqrt%s%ssqrt%s)/(sqrt%s%ssqrt%s)' 
                                      % (first_root, opp_val, second_root,
                                         first_root, opp_val, second_root)))
    comb_step = tostring(am.parse('(%s*(sqrt%s%ssqrt%s))/((sqrt%s%ssqrt%s) \
                                  (sqrt%s%ssqrt%s))' % (numerator, 
                                                        first_root, 
                                                        opp_val,
                                                        second_root, 
                                                        first_root, 
                                                        type_val, 
                                                        second_root, 
                                                        first_root, 
                                                        opp_val, 
                                                        second_root)))
    binom_denom = tostring(am.parse('(sqrt%s%ssqrt%s)(sqrt%s%ssqrt%s)' 
                                    % (first_root, 
                                       type_val, 
                                       second_root, 
                                       first_root, 
                                       opp_val, 
                                       second_root)))
    binom_root = \
    simplify((sqrt(first_root)+sqrt(second_root))*
             (sqrt(first_root)-sqrt(second_root)))
    binom_root_str = tostring(am.parse(str(binom_root)))
    binom_sq_root = tostring(am.parse('((sqrt%s)^2-(sqrt%s)^2) =' 
                                      % (first_root, second_root)))
    binom_sq_root_solv = tostring(am.parse('(%s-%s) =' % (first_root, 
                                                          second_root)))
    steps.append('Multiply both numerator and denominator by %s' % step_print) 
    steps.append('Meaning %s %s %s' % (question_print,
                                           tostring(am.parse('*')),
                                           step_multiply))
    steps.append('Resulting in %s' % comb_step)
    steps.append('Note %s' % tostring(am.parse('(a+b)(a-b) = a^2-b^2')))
    steps.append('Therefore denominator %s becomes %s %s %s' 
                 % (binom_denom, binom_sq_root, binom_sq_root_solv, binom_root_str))
    answer = []
    answer.append(steps)
    ans_val = None
    if not type_denom:
        ans_val = radsimp(numerator/(sqrt(first_root)-sqrt(second_root)))
    else:
        ans_val = radsimp(numerator/(sqrt(first_root)+sqrt(second_root)))
    ans_val = together(ans_val)
    val_regex = re.compile("[0-9]+\*{2}\(1\/2\)")
    val_regex_yank = re.compile("\*{2}\(1\/2\)")
    match = val_regex.split(str(ans_val))
    yank_vals = val_regex.findall(str(ans_val))
    for index, item in enumerate(yank_vals):
        yank_vals[index] = re.sub("\*{2}\(1\/2\)", "", str(item))

    val_regex_neg = re.compile("-")
    val_neg = val_regex_neg.findall(str(match[0][1:]))
    if len(val_neg):
        if val_neg[0] == '-' and match[1] == ' - ':
            ans_val = "-" + match[0][0] + re.sub("-", "", match[0][1:]) + \
                    "sqrt" + yank_vals[0] + " + "
        else:
            ans_val = match[0] + "sqrt" + yank_vals[0] + match[1]
    else:
        ans_val = match[0] + "sqrt" + yank_vals[0] + match[1]

    if len(match) > 2:
        ans_val += "sqrt" + yank_vals[1] + match[2]
    answer.append(tostring(am.parse(str(ans_val).replace("**","^"))))

    return question, answer

def qGrpDifferentiation_template():
    '''Group Differentiation  e.g. diff x^2*e^x'''
    #TODO: Need to make this more random selection
    #TODO: tan not working. It's supposed to give sec^2 as answer
    type_diff1 = randint(0,3) #normal,exp,trig,log
    type_diff2 = randint(0,3) #normal,exp,trig,log
    first_part =  None
    second_part =  None

    if type_diff1 == 0:
        first_part = exp(x**(randint(2,100)) + randint(-100,100))
    elif type_diff1 == 1:
        first_part = exp(x**(randint(2,100)) + randint(-100,100))
    elif type_diff1 == 2:
        #TODO BUG: tan NOT giveing right values
        #sohcahtoa_type = randint(0,2) #Sine,Cosine,Tan
        sohcahtoa_type = randint(0,1) #Sine,Cosine
        if sohcahtoa_type == 0:
            first_part = sin(x**(randint(2,100))+randint(-100,100))
        if sohcahtoa_type == 1:
            first_part = cos(x**(randint(2,100))+randint(-100,100))
        if sohcahtoa_type == 2:
            first_part = tan(x**(randint(2,100))+randint(-100,100))
    elif type_diff1 == 3:
        first_part = ln((randint(2,100)*x+randint(-100,100)))

    if type_diff2 == 0:
        second_part = exp(x**(randint(2,100)) + randint(-100,100))
    elif type_diff2 == 1:
        second_part = exp(x**(randint(2,100)) + randint(-100,100))
    elif type_diff2 == 2:
        #TODO BUG: tan NOT giveing right values
        #sohcahtoa_type = randint(0,2) #Sine,Cosine,Tan
        sohcahtoa_type = randint(0,1) #Sine,Cosine
        if sohcahtoa_type == 0:
            second_part = sin(x**(randint(2,100))+randint(-100,100))
        if sohcahtoa_type == 1:
            second_part = cos(x**(randint(2,100))+randint(-100,100))
        if sohcahtoa_type == 2:
            second_part = tan(x**(randint(2,100))+randint(-100,100))
    elif type_diff2 == 3:
        second_part = ln((randint(2,100)*x+randint(-100,100)))
    first_part_str = str(first_part).replace("exp","e^").replace("log", "ln").replace("**", "^").replace("(", "((").replace(")", "))")
    second_part_str = str(second_part).replace("exp","e^").replace("log","ln").replace("**","^").replace("(", "((").replace(")", "))")
    question = 'Differentiate ' + tostring(am.parse('%s*%s' 
                                                    % (first_part_str, 
                                                       second_part_str))) 
    question += ' with respect to ' + tostring(am.parse('x'))

    steps = []
    first_part_diff = diff(first_part)
    second_part_diff = diff(second_part)
    first_part_diffstr = str(first_part_diff).replace("exp","e^").replace("log", "ln").replace("**", "^").replace("(", "((").replace(")", "))")
    second_part_diffstr = str(second_part_diff).replace("exp","e^").replace("log","ln").replace("**","^").replace("(", "((").replace(")", "))")
    steps.append('This is a group differentiation')
    steps.append('Differentiate %s and multiply it to %s' %
                 (tostring(am.parse(first_part_str)),
                  tostring(am.parse(second_part_str))))
    steps.append('This will give %s%s  -> part (a)' %
                 (tostring(am.parse(first_part_diffstr)),
                 tostring(am.parse('*'+second_part_str))))
    steps.append('Similarly, differentiate %s and multiply it to %s' %
                 (tostring(am.parse(second_part_str)),
                  tostring(am.parse(first_part_str))))
    steps.append('This will give %s%s  -> part (b)' %
                 (tostring(am.parse(second_part_diffstr)),
                 tostring(am.parse('*'+first_part_str))))
    steps.append('Add part(a) and (b) together')
    answer = []
    answer.append(steps)
    if second_part_diffstr[0] == '-':
        answer.append(tostring(am.parse('%s%s%s%s' % (first_part_diffstr,
                                                      second_part_str,
                                                      second_part_diffstr,
                                                      first_part_str))))
    else:
        answer.append(tostring(am.parse('%s%s+%s%s' % (first_part_diffstr,
                                                       second_part_str,
                                                       second_part_diffstr,
                                                       first_part_str))))

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
    steps.append('This will give %s which is mulitiplied to original question' 
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
    while first_val == 0:
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
    diff_inside = diff(first_val*x+second_val)
    if second_val < 0:
        steps.append('Differentiate %s normally' % tostring(am.parse('%sx%s' %
                                                   (first_val, second_val))))
    else:
        steps.append('Differentiate %s normally' % tostring(am.parse('%sx+%s' %
                                                   (first_val, second_val))))
    steps.append('This will give %s which goes as numerator' % str(diff_inside))
    if second_val < 0:
        steps.append('%s goes as denominator' % tostring(am.parse('%sx%s' %
                                                   (first_val, second_val))))
    else:
        steps.append('%s goes as denominator' % tostring(am.parse('%sx+%s' %
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
    steps.append('Then you need to square root the answer.')
    steps.append('Use either [1/y] key or similar on calculator and press ' 
                 + str(root_val))
    steps.append('Please refer to your calculator manual if in doubt.')
    steps.append('Then look for %s significant figures.' % sig_fig)
    steps.append('Note: First non-zero digit is 1st signifiant figure,' + \
                 ' going from left to right. Each digit after that is a' + \
                 ' significant figure.')
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
    x = Symbol('x', real=True) #For 4U Maths use complex=True for ImaginaryNum
    question_str = "Solve "
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
    answer.append(tostring(am.parse(str(solve(question, x)))))

    return question_str, answer

def qExponentialSameBase_template():
    '''Solves the same base e.g. 2^(2x+1) = 32.'''
    base = choice([2,3,5,7])
    pow_rs = randint(3,6)
    rs = int(pow(base,pow_rs))
    front_num = randint(-100,100)
    while front_num == 0:
        front_num = randint(-100,100)
    lspow = front_num*x+randint(-100,100)
    question = 'Solve ' + tostring(am.parse('%s^(%s) = %s' % (base, lspow, rs)))
    ls_samebase = tostring(am.parse('%s^(%s)' % (base, lspow)))
    rs_samebase = tostring(am.parse('%s^(%s)' % (base, pow_rs)))
    steps = []
    steps.append('Covert right side to be same base as left side. Left side' \
                 ' has a base of: ' + str(base))
    steps.append('As ' + tostring(am.parse('%s^(%s)=%s' % 
                                                 (base, pow_rs, rs))))
    steps.append('Right side is now: ' + tostring(am.parse('%s^(%s)' % 
                                                           (base, pow_rs))))
    steps.append('Therefore ' + ls_samebase + tostring(am.parse('=')) + \
                 rs_samebase)
    steps.append('Therefore solve: ' + tostring(am.parse('%s%s%s' %
                                                        (lspow,'=',pow_rs)))) 
    steps.append('Note: As bases are same the power equates to each other.')
    answer = []
    answer.append(steps)

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

    #Start - 2nd Iteration
    #q, a = qIntegrationNegativePower_template()
    #questions.append(q)
    #answers.append(a)

    #q, a = qSimpleBatchProbability_template()
    #questions.append(q)
    #answers.append(a)

    #Start - 1st Iteration
    q, a = qRationaliseDenominator_template()
    questions.append(q)
    answers.append(a)

    q, a = qGrpDifferentiation_template()
    questions.append(q)
    answers.append(a)

    q, a = qSimplifyBinomial_template()
    questions.append(q)
    answers.append(a)

    q, a = qSignificantFigures_template()
    questions.append(q)
    answers.append(a)

    q, a = qExpDifferentiation_template()
    questions.append(q)
    answers.append(a)

    q, a = qExponentialSameBase_template()
    questions.append(q)
    answers.append(a)

    q, a = qInequalities_template()
    questions.append(q)
    answers.append(a)

    q, a = qLogDifferentiation_template()
    questions.append(q)
    answers.append(a)

    render_question_paper(questions, answers)

    

if __name__ == '__main__':
    main()
