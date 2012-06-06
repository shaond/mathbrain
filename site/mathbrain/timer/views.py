from random import choice
from django.http import HttpResponse
from django.core import serializers
from models import Question


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

                qid = []
                questions = []
                marks = 12
                qset = Question.objects.filter(subject=subject, num=1).order_by('?')
                q1 = qset[0]
                questions.append(q1)
                qid.append(q1.id)
                
                marks = marks - q1.mark
                while marks != 0:
                    nxt_q = qset.filter(mark__lte=marks).exclude(id__in=qid)[0]
                    questions.append(nxt_q)
                    qid.append(nxt_q.id)
                    marks = marks - nxt_q.mark

                data = serializers.serialize('json', questions)
                return HttpResponse(data, mimetype='application/json')
        return HttpResponse("Error", mimetype='application/json')
