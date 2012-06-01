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
