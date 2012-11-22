# mquiz/views.py
from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.contrib.auth import (authenticate, logout, views)
from django.contrib.auth.models import User
from django.forms.formsets import formset_factory
from django.http import HttpResponseRedirect
from django.contrib import messages

from mquiz.models import Quiz
from forms import QuizForm, QuestionForm

def home_view(request):
    latest_quiz_list = Quiz.objects.filter(draft=0).order_by('-created_date')[:10]
    return render_to_response('mquiz/home.html',{'latest_quiz_list': latest_quiz_list}, context_instance=RequestContext(request))

def create_quiz(request):
    #QuestionFormSet = formset_factory(QuestionForm,extra=3,)
    if request.method == 'POST':
        quiz_form = QuizForm(request.POST)
        #question_formset = QuestionFormSet(request.POST,prefix='questions')
        if quiz_form.is_valid():
            quiz = quiz_form.save(commit=False)
            quiz.owner_id = request.user.id
            quiz.save()
            messages.info(request, "Your quiz was saved")
            return HttpResponseRedirect('saved/')
    else:
        quiz_form = QuizForm() # An unbound form
        #question_formset = QuestionFormSet(prefix='questions',)
        

    return render(request, 'mquiz/quiz/quiz.html', {'quiz_form': quiz_form,})



