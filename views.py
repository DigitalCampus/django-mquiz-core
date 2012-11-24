# mquiz/views.py
from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.contrib.auth import (authenticate, logout, views)
from django.contrib.auth.models import User
from django.forms.formsets import formset_factory
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.conf import settings

from mquiz.models import Quiz, Question, Response
from forms import QuizForm, QuestionForm, ResponseForm,BaseQuestionFormSet

def home_view(request):
    latest_quiz_list = Quiz.objects.filter(draft=0).order_by('-created_date')[:10]
    return render_to_response('mquiz/home.html',{'latest_quiz_list': latest_quiz_list}, context_instance=RequestContext(request))

def about_view(request):
        return render_to_response('mquiz/about.html', 
                                  {'settings': settings},
                                  context_instance=RequestContext(request))
def contact_view(request):
        return render_to_response('mquiz/contact.html', 
                                  {'settings': settings},
                                  context_instance=RequestContext(request))
        
def terms_view(request):
        return render_to_response('mquiz/terms.html', 
                                  {'settings': settings},
                                  context_instance=RequestContext(request))
                     
def create_quiz(request):
    QuestionFormSet = formset_factory(QuestionForm,extra=5,formset=BaseQuestionFormSet)
    
    if request.method == 'POST':
    
        quiz_form = QuizForm(request.POST)
        question_formset = forms.QuestionFormSet(request.POST,)
        
        if quiz_form.is_valid():
            quiz = quiz_form.save(commit=False)
            quiz.owner = request.user
            quiz.save()
            
            #if question_formset.is_valid():
                # do something here 
                     
            #return HttpResponseRedirect('saved/')
    else:
        quiz_form = QuizForm() # An unbound form
        question_formset = QuestionFormSet()

    return render(request, 'mquiz/quiz/quiz.html', {'quiz_form': quiz_form,'question_formset':question_formset})



