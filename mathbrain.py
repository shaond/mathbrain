#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asciimathml as am

from xml.etree.ElementTree import tostring
from jinja2 import Environment, PackageLoader
from sympy import solve, Poly, Eq, Function, exp, Le, Lt, Ge, Gt
from sympy import pi, cse, sqrt, simplify, diff, ln, sin, cos, tan
from sympy import radsimp, factor, together, Symbol, integrate, real_roots
from sympy.mpmath import nthroot, root
from sympy.printing import mathml
from sympy.abc import x, y
from random import choice, randint
from math import pow, log10, floor
import re

def qQuadAlphBeta_template():
    '''Find Alpha & Beta in Quadratic Equation 
    e.g. The quadratic equation x2 – 6x + 2 = 0 has roots α and β.'''
    a_part = randint(-10, 10)
    while a_part == 0 or a_part == 1: 
        a_part = randint(-10, 10)
    b_part = randint(-100,100)
    while b_part == 0: 
        b_part = randint(-100,100)

    c_part = randint(-100,100)
    #This is so that b^2-4ac is always positive
    if a_part > 0:
        c_part = randint(-100, -2)
    else:
        c_part = randint(2,100)

    alpha_str = tostring(am.parse("alpha"))
    beta_str = tostring(am.parse("beta"))
    question = "The quadratic equation  " 
    question_eqn = None
    first_qn = tostring(am.parse("alpha+beta"))
    second_qn = tostring(am.parse("alphabeta"))
    third_qn = tostring(am.parse("1/(alpha)+1/(beta)"))
    if b_part > 0 and c_part > 0: 
        question_eqn = tostring(am.parse("%sx^2+%sx+%s=0" % (str(a_part), 
                                                            str(b_part), 
                                                            str(c_part))))
    elif b_part > 0 and c_part < 0: 
        question_eqn = tostring(am.parse("%sx^2+%sx%s=0" % (str(a_part), 
                                                           str(b_part),
                                                           str(c_part))))
    elif b_part < 0 and c_part < 0: 
        question_eqn = tostring(am.parse("%sx^2%sx%s=0" % (str(a_part), 
                                                          str(b_part), 
                                                          str(c_part))))
    else: 
        question_eqn = tostring(am.parse("%sx^2%sx+%s=0" % (str(a_part), 
                                                           str(b_part), 
                                                           str(c_part))))
    question += question_eqn 
    question += " has roots %s and %s."  % (alpha_str, beta_str) 
    question += " (i) Find " + first_qn 
    question += " (ii) Find " + second_qn
    question += " (iii) Find " + third_qn

    steps = []
    ans_val = real_roots(a_part*x**2+b_part*x+c_part)
    alpha_root, beta_root = ans_val[0], ans_val[1]
    part_i_ans = simplify(alpha_root + beta_root)
    part_ii_ans = simplify(alpha_root * beta_root)
    part_iii_ans = "(%s)/(%s)" % (str(part_i_ans).replace("**","^"),
                                  str(part_ii_ans).replace("**","^"))
    quad_eqn_formula = tostring(am.parse("(-b+-sqrt(b^2-4ac))/(2a)"))
    steps.append("First find the roots to alpha and beta")
    steps.append("This is found by using the quadratic formula " +
                 quad_eqn_formula)
    steps.append("Note discrimant %s has to be +ve to have 2 real roots" % \
                 tostring(am.parse("b^2-4ac")))
    steps.append("%s is in the quadratic form %s" % \
                 (question_eqn, tostring(am.parse("ax^2+bx+c=0"))))
    steps.append("As %s is equal to %s, respectively" % \
                 (tostring(am.parse("a,b,c")), 
                           tostring(am.parse("%s,%s,%s" % (str(a_part), 
                                                           str(b_part), 
                                                           str(c_part))))))
    steps.append("Substitute %s into %s" % (tostring(am.parse("%s,%s,%s" %
                                                              (str(a_part),
                                                               str(b_part),
                                                               str(c_part)))), 
                                            quad_eqn_formula))
    steps.append("This gives" +
                 tostring(am.parse("(-(%s)+-sqrt((%s)^2-4(%s)(%s)))/(2(%s))" %
                                   (str(b_part), str(b_part), str(a_part),
                                    str(c_part), str(a_part)))))
    steps.append("**For our answers, we might have used power of 1/2. Please" +
                 " replace with square root instead") 
    steps.append("Which gives " + 
                 tostring(am.parse("%s, %s" % 
                                   (str(alpha_root).replace("**","^"), 
                                    str(beta_root).replace("**", "^")))) + 
                 " which are the 2 real roots known as alpha and beta")
    steps.append("Part (i) is solved by " + \
                 tostring(am.parse("%s+(%s)=%s" % \
                                   (str(alpha_root).replace("**","^"), 
                                    str(beta_root).replace("**", "^"),
                                    str(part_i_ans).replace("**","^"))))) 
    steps.append("Part (ii) is solved by " + \
                 tostring(am.parse("%s*(%s)=%s" % \
                                   (str(alpha_root).replace("**","^"), 
                                    str(beta_root).replace("**", "^"),
                                    str(part_ii_ans).replace("**","^"))))) 
    steps.append("Part (iii) %s is equivalent to %s therefore using results " \
                 "from part (i) & (ii): %s" %  
                 (third_qn, tostring(am.parse("(alpha+beta)/(alpha*beta)")),
                  tostring(am.parse(part_iii_ans))))

    answer = []
    answer.append(steps)
    answer.append(tostring(am.parse(str("%s,%s,%s" % (str(part_i_ans).replace("**","^"),
                                                      str(part_ii_ans).replace("**","^"),
                                                      part_iii_ans)))))

    return question, answer

def qEquationTangent_template():
    '''Equation of Tangent e.g. Find the equation of the tangent to the curve 
    y = (2x + 1)^4 at the point where x = –1.'''
    front_x = randint(-6, 7)
    while front_x == 0 or front_x == 1 or front_x == -1: 
        front_x = randint(-6, 7)
    attach_val = randint(-100,100)
    while attach_val == 0: 
        attach_val = randint(-100,100)
    pow_val = choice([2,4,6])

    x_val = randint(-2,3)

    question = "Find the equation of the tangent to the curve " 
    question_eqn = None
    if attach_val > 0: 
        question_eqn = tostring(am.parse("y=(%sx+%s)^%s" % (str(front_x), 
                                                            str(attach_val), 
                                                            str(pow_val))))
    else: 
        question_eqn = tostring(am.parse("y=(%sx%s)^%s" % (str(front_x), 
                                                           str(attach_val), 
                                                           str(pow_val)))) 
    question += question_eqn 
    question += " at the point where " 
    question += tostring(am.parse("x=%s" % str(x_val)))

    steps = []
    straight_line_eqn = tostring(am.parse("y-y_1=m(x-x_1)"))
    steps.append("Equation of a tangent is based on " + straight_line_eqn)
    steps.append("%s, the gradient can be found by differentation of %s and \
                 substituting %s" %
                 (tostring(am.parse("m")), 
                  question_eqn, tostring(am.parse("x=%s" % str(x_val)))))
    diff_eqn = diff((front_x*x+attach_val)**pow_val)
    m_val = diff_eqn.subs(x,x_val)
    y_val = (front_x*x_val+attach_val)**pow_val
    steps.append(tostring(am.parse("m=%s" % str(diff_eqn).replace("**","^"))) 
                 + " substituting " + tostring(am.parse("x=%s" % str(x_val))))
    steps.append("Therefore %s " % tostring(am.parse("m=%s" % str(m_val))))
    steps.append("Now " + tostring(am.parse("x_1=%s" % str(x_val))))
    steps.append("Need to find " + tostring(am.parse("y_1")))
    steps.append("Find "  + tostring(am.parse("y_1")) + "by solving " +
                 question_eqn + "with " + tostring(am.parse("x_1")))
    steps.append("Therefore "  + tostring(am.parse("y_1")) + "by solving " +
                 question_eqn + "where " + tostring(am.parse("x=x_1")))
    steps.append(tostring(am.parse("y_1=%s" % str(y_val))))
    steps.append("Therefore rearrange " + tostring(am.parse("y-(%s)=%s(x+(%s))" 
                                                            % (str(y_val), 
                                                               str(m_val), 
                                                               str(x_val)))))

    answer = []
    answer.append(steps)
    ans_val = simplify(m_val*(x+x_val)+y_val)
    answer.append(tostring(am.parse(str("y=%s" % str(ans_val))
                                    .replace("**","^"))))

    return question, answer

def qDefiniteIntegralLog_template():
    '''Definite Integral Log e.g. Integrate 5/x with e^3,e'''
    numerator = randint(-100, 100)
    while numerator == 0 or numerator == 1: 
        numerator = randint(-100, 100)
    denominator = randint(-100,100)
    if numerator < 0:
        denominator = randint(2,100)
    else:
        while denominator == 0  or denominator == 1: 
            denominator = randint(-100,100)
    max_val_pow = randint(-100,100)
    while max_val_pow == 0 or max_val_pow == 1: 
        max_val_pow = randint(-100,100)
    min_val_pow = randint(-100,100)
    while min_val_pow > max_val_pow: 
        min_val_pow = randint(-100,100)

    question = "Evaluate " 
    if min_val_pow == 0: 
        question += tostring(am.parse('int_(0)^(e^%s)%s/(%sx)dx' % 
                                      (str(max_val_pow),
                                       str(numerator),
                                       str(denominator))))
    elif min_val_pow == 1: 
        question += tostring(am.parse('int_(e)^(e^%s)%s/(%sx)dx' % 
                                      (str(max_val_pow),
                                       str(numerator),
                                       str(denominator))))
    else: 
        question += tostring(am.parse('int_(e^%s)^(e^%s)%s/(%sx)dx' % 
                                      (str(min_val_pow),
                                       str(max_val_pow),
                                       str(numerator),
                                       str(denominator))))

    steps = []
    num_log_diff = diff(denominator*x)
    true_log_integrate = tostring(am.parse('int1/x'))
    fudge_factor = tostring(am.parse("%s/%s" % (str(numerator),
                                                str(denominator))))
    steps.append("This is a logarithmic integration.")
    steps.append("The reason is that the numerator's x-power is " + \
                 "one less than the x power of the denominator. " + \
                 "The integration looks similar to this " + \
                 true_log_integrate)
    steps.append("Note that the numerator is different to the one we expect" \
                 " and we need to take out fudge factor which is " \
                 + fudge_factor)
    steps.append("This results in " + \
                 tostring(am.parse('(1/%s)*%s*int_(e^%s)^(e^%s)1/xdx' % 
                                   (str(denominator),
                                    str(numerator),
                                    str(min_val_pow),
                                    str(max_val_pow)))))
    steps.append("Which gives " + \
                 tostring(am.parse('(%s/%s)*[ln((x))]_(e^%s)^(e^%s)' % 
                                   (str(numerator),
                                    str(denominator),
                                    str(min_val_pow),
                                    str(max_val_pow)))))
    steps.append("Which equals " + \
                 tostring(am.parse('(%s/%s)*[ln((e^%s)) - ln((e^%s))]' % 
                                   (str(numerator),
                                    str(denominator),
                                    str(max_val_pow),
                                    str(min_val_pow)))))

    answer = []
    answer.append(steps)
    ans_val = integrate(numerator/(denominator*x), (x, exp(min_val_pow),
                                                    exp(max_val_pow)))
    answer.append(tostring(am.parse(str(ans_val).replace("**","^"))))

    return question, answer

def qDifferentiationSimpleTrig_template():
    '''Differentiation involving trigonometry e.g. diff sin(x^2-2x).dx'''
    x_pow = randint(2,100) 
    front_x = randint(-100,100) 
    #TODO BUG: tan NOT giveing right values
    #sohcahtoa_type = randint(0,2) #Sine,Cosine,Tan
    sohcahtoa_type = randint(0,1) #Sine,Cosine
    ans_val = None 
    if sohcahtoa_type == 0:
        ans_val = diff(sin(x**x_pow+front_x*x))
    if sohcahtoa_type == 1:
        ans_val  = diff(cos(x**x_pow+front_x*x))
    if sohcahtoa_type == 2:
        ans_val = diff(tan(x**x_pow+front_x*x))

    question = None
    if front_x > 0 and sohcahtoa_type == 0:
        question = "Differentiate " + tostring(am.parse('sin((x^%s+%s*x))'%
                                                        (str(x_pow),
                                                         str(front_x))))
    elif front_x < 0 and sohcahtoa_type == 0:
        question = "Differentiate " + tostring(am.parse('sin(x^%s%s*x)'%
                                                        (str(x_pow),
                                                         str(front_x))))
    elif front_x > 0 and sohcahtoa_type == 1:
        question = "Differentiate " + tostring(am.parse('cos((x^%s+%s*x))'%
                                                        (str(x_pow),
                                                         str(front_x))))
    elif front_x < 0 and sohcahtoa_type == 1:
        question = "Differentiate " + tostring(am.parse('cos((x^%s%s*x))'%
                                                        (str(x_pow),
                                                         str(front_x))))
    elif front_x > 0 and sohcahtoa_type == 2:
        question = "Differentiate " + tostring(am.parse('tan((x^%s+%s*x))'%
                                                        (str(x_pow),
                                                         str(front_x))))
    elif front_x < 0 and sohcahtoa_type == 2:
        question = "Differentiate " + tostring(am.parse('tan((x^%s%s*x))'%
                                                        (str(x_pow),
                                                         str(front_x))))
    question += " with respect to x"


    steps = []
    steps.append("This is a trigonometry differentiation question.")
    steps.append("Note a diff of sin(*) gives cos(*) whereas a diff of" + \
                 " cos(*) gives -sin(*). Diff of tan gives sec squared.")
    steps.append("Differentiate the inside and multiply it to the value of" + \
                 " the outside")

    answer = []
    answer.append(steps)
    trig_regex = re.compile("sin\(|cos\(")
    match_obj = trig_regex.split(str(ans_val))
    sin_cos_val = match_obj[0]
    if 'cos' in str(ans_val):
        sin_cos_val += "cos(("
    if 'sin' in str(ans_val):
        sin_cos_val += "sin(("
    sin_cos_val += match_obj[1]
    sin_cos_val += ")"
    sin_cos_val = re.sub("-\(-","(",sin_cos_val)
    answer.append(tostring(am.parse(str(sin_cos_val).replace("**","^"))))

    return question, answer

def qDifferentiationHardTrig_template():
    '''Differentiation involving trigonometry e.g. diff x/sin(x^2).dx'''
    x_pow = randint(2,100) 
    front_x_denom = randint(-100,100) 
    while front_x_denom == 0:
        front_x_denom = randint(-100,100) 
    front_x_num = randint(-100,100) 
    while front_x_num  == 0:
        front_x_num  = randint(-100,100) 

    #TODO BUG: tan NOT giveing right values
    #sohcahtoa_type = randint(0,2) #Sine,Cosine,Tan
    sohcahtoa_type = randint(0,1) #Sine,Cosine
    ans_val = None 
    denominator = None 
    question = None 
    numerator = front_x_num*x 

    if sohcahtoa_type == 0:
        denominator = sin(x**x_pow+front_x_denom*x)
    if sohcahtoa_type == 1:
        denominator = cos(x**x_pow+front_x_denom*x)

    ans_val = simplify(diff(numerator/denominator))

    if sohcahtoa_type == 0 and front_x_denom > 0:
        question = "Differentiate " + tostring(am.parse('(%s*x)/ \
                                                        sin((x^%s+%s*x))'% 
                                                        (str(front_x_num),
                                                         str(x_pow),
                                                         str(front_x_denom))))
    elif sohcahtoa_type == 0 and front_x_denom < 0:
        question = "Differentiate " + tostring(am.parse('(%s*x)/ \
                                                        sin((x^%s%s*x))'% 
                                                        (str(front_x_num),
                                                         str(x_pow),
                                                         str(front_x_denom))))
    elif sohcahtoa_type == 1 and front_x_denom > 0:
        question = "Differentiate " + tostring(am.parse('(%s*x)/ \
                                                        cos((x^%s+%s*x))'% 
                                                        (str(front_x_num),
                                                         str(x_pow),
                                                         str(front_x_denom))))
    elif sohcahtoa_type == 1 and front_x_denom < 0:
        question = "Differentiate " + tostring(am.parse('(%s*x)/ \
                                                        cos((x^%s%s*x))'% 
                                                        (str(front_x_num),
                                                         str(x_pow),
                                                         str(front_x_denom))))
    question += " with respect to x"

    steps = []
    denominator_diff = diff(denominator)
    numerator_diff = diff(numerator)
    quotient_rule = tostring(am.parse("(v*u'-u*v')/(v^2)"))
    trig_regex = re.compile("sin\(|cos\(")
    match_obj = trig_regex.split(str(denominator_diff))
    sin_cos_val = match_obj[0]
    if 'cos' in str(denominator_diff):
        sin_cos_val += "cos(("
    if 'sin' in str(denominator_diff):
        sin_cos_val += "sin(("
    sin_cos_val += match_obj[1]
    sin_cos_val += ")"
    sin_cos_val = re.sub("-\(-","(",sin_cos_val)

    steps.append("This is a differentiation of denominator and numerator")
    steps.append("This is based on diff of " + tostring(am.parse('u/v')) + \
                 " which is " + quotient_rule) 
    steps.append("Please refer to http://en.wikipedia.org/wiki/Quotient_rule")
    steps.append(tostring(am.parse("v'=%s" %
                                   str(sin_cos_val).replace("**","^"))))
    steps.append(tostring(am.parse("u'=%s" % str(numerator_diff)))) 
    ans_val = str(ans_val).replace("**","^").replace("(","((").replace(")","))")
    ans_val = ans_val.replace("/","/(").replace(")^2",")^2)")

    answer = []
    answer.append(steps)
    answer.append(tostring(am.parse(ans_val)))
    return question, answer

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
    steps.append("This gives %s" % str(float(num_items)*defective_prob))
    steps.append("Round to nearest whole number as you cannot have fraction")

    answer = []
    answer.append(steps)
    ans = int(round(float(float(num_items)*defective_prob),0))
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
    q, a = qQuadAlphBeta_template()
    questions.append(q)
    answers.append(a)

    q, a = qEquationTangent_template()
    questions.append(q)
    answers.append(a)

    q, a = qDefiniteIntegralLog_template()
    questions.append(q)
    answers.append(a)

    q, a = qDifferentiationHardTrig_template()
    questions.append(q)
    answers.append(a)

    q, a = qDifferentiationSimpleTrig_template()
    questions.append(q)
    answers.append(a)

    q, a = qIntegrationNegativePower_template()
    questions.append(q)
    answers.append(a)

    q, a = qSimpleBatchProbability_template()
    questions.append(q)
    answers.append(a)

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
