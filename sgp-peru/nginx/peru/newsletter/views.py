from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import NewsLetter
from .models import NewsLetter

def newsletter(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        mail=request.POST['mail']
        q = NewsLetter(
            mail = mail
        )
        q.save()
        return HttpResponseRedirect('/')