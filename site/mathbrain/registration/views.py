from django.http import HttpResponse
from models import Registration

def index(request):
    if request.method == 'POST':
        email = request.GET.get('email_registration')
        if email:
            reg = Registration.objects.create(email=email)
            reg.save()
            return HttpResponse("Success", mimetype='application/json')
        return HttpResponse("Error", mimetype='application/json')
