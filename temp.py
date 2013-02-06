# mquiz/temp.py
from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.contrib.auth import (authenticate, logout, views)
from django.contrib.auth.models import User
from django.forms.formsets import formset_factory
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.conf import settings
from django.http import Http404
from django.core.mail import send_mail


def tracker(request):
    data = request.POST.items()
    send_mail('mQuiz: Request to old Tracker api', 'Sent:' + data, 
                      settings.SERVER_EMAIL, [settings.SERVER_EMAIL], fail_silently=True)
    return render_to_response('mquiz/temp.html')

def submit(request):
    data = request.POST.items()
    send_mail('mQuiz: Request to old Submit api', 'Sent:' + data, 
                      settings.SERVER_EMAIL, [settings.SERVER_EMAIL], fail_silently=True)
    return render_to_response('mquiz/temp.html')