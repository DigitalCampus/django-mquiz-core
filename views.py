#mquiz/views.py
from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.contrib.auth import (authenticate, logout, views)
from django.contrib.auth.models import User

from mquiz.models import Quiz
from forms import QuizForm

def home_view(request):
    latest_quiz_list = Quiz.objects.all().order_by('-created_date')[:10]
    return render_to_response('mquiz/home.html',{'latest_quiz_list': latest_quiz_list}, context_instance=RequestContext(request))

def create(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
    else:
        form = QuizForm() # An unbound form

    return render(request, 'mquiz/quiz/quiz.html', {'form': form,})



