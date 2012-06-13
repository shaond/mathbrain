from django.views.decorators.csrf import requires_csrf_token
from django.shortcuts import render
from django.http import HttpResponse
from models import Registration

def index(request):
    if request.method == 'POST':
        email = request.POST.get('email_registration')
        if email:
            reg = Registration.objects.create(email=email)
            reg.save()
            return render(request, "registration_success.html")
        return render(request, "registration_error.html")
