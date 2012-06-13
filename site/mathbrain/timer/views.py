from random import choice
from django.http import HttpResponse
from django.core import serializers
from models import Question

import os 
from topics import TwoUnit, ThreeUnit, FourUnit

def png_to_model(request):
    '''Populate a model based on filename'''
    path_img = os.path.join(os.pardir, 'mathbrain/questions')
    for filename in os.listdir(path_img):
        vals = filename.split("_") 
        topic_vals = vals[6].split(".png")[0]
        if vals[0] == "2u":
            topic_vals = TwoUnit.topics[int(topic_vals)]
        elif vals[0] == "3u":
            topic_vals = ThreeUnit.topics[int(topic_vals)]
        elif vals[0] == "4u":
            topic_vals = FourUnit.topics[int(topic_vals)]
        new_qn = Question(question_img="questions/"+filename, 
                         num=int(vals[2][1:]), 
                         mark=int(vals[4].split("m")[0]), 
                         subject=int(vals[0][0]), 
                         source=vals[5], 
                         topic=topic_vals, 
                         pub_date=vals[1]+'-01-01')
        new_qn.save()

    return HttpResponse("Done", mimetype='application/json')

def questionset(subject=2):
    questions = []
    marks_start = 0
    num_questions = 0

    if int(subject) == 2: #2U Maths
        marks_start = 12
        num_questions = 10
    elif int(subject) == 3: #3U Maths
        marks_start = 12
        num_questions = 7
    elif int(subject) == 4: #4U Maths
        marks_start = 15
        num_questions = 8

    for qnum in range(num_questions):
        qset = Question.objects.filter(subject=subject, num=qnum+1).order_by('?')
        q1 = qset[0]
        questions.append(q1)
        qid = []
        qid.append(q1.id)
        
        marks = marks_start - q1.mark
        while marks != 0:
            try:
                nxt_q = qset.filter(mark__lte=marks).exclude(id__in=qid)[0]
                questions.append(nxt_q)
                qid.append(nxt_q.id)
                marks = marks - nxt_q.mark
            except IndexError: #This can happen if we don't get 'exactly' total
                marks -= marks
    return questions

def index(request):
    if request.method == 'GET':
        question_number = request.GET.get('number')
        question_mark = request.GET.get('mark')
        subject = request.GET.get('subject')
        if question_mark and question_number and subject:
            if question_number.isdigit() and question_mark.isdigit():
                question = Question.objects.filter(num=question_number, mark=question_mark, subject=subject)
                data = serializers.serialize('json', question)
                return HttpResponse(data, mimetype='application/json')
        return HttpResponse("Error", mimetype='application/json')

def buildexam(request, subject):
    if request.method == 'GET':
        if subject:
            if subject.isdigit():
                data = serializers.serialize('json', questionset(subject))
                return HttpResponse(data, mimetype='application/json')
        return HttpResponse("Error, subject: %s" % subject, mimetype='application/json')
