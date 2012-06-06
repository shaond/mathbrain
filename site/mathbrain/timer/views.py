from random import choice
from django.http import HttpResponse
from django.core import serializers
from models import Question


def questionset(subject=2):
    qid = []
    questions = []
    marks = 0
    num_questions = 0

    if int(subject) == 2: #2U Maths
        marks = 12
        num_questions = 10
    elif int(subject) == 3: #3U Maths
        marks = 12
        num_questions = 7
    elif int(subject) == 4: #4U Maths
        marks = 15
        num_questions = 8

    for qnum in range(num_questions):
        qset = Question.objects.filter(subject=subject, num=qnum).order_by('?')
        q1 = qset[0]
        questions.append(q1)
        qid.append(q1.id)
        
        marks = marks - q1.mark
        while marks != 0:
            nxt_q = qset.filter(mark__lte=marks).exclude(id__in=qid)[0]
            questions.append(nxt_q)
            qid.append(nxt_q.id)
            marks = marks - nxt_q.mark
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

def buildexam(request):
    if request.method == 'GET':
        subject = request.GET.get('subject')
        if subject:
            if subject.isdigit():
                data = serializers.serialize('json', questionset(subject))
                return HttpResponse(data, mimetype='application/json')
        return HttpResponse("Error", mimetype='application/json')
