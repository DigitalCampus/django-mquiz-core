# mquiz/views.py
from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.contrib.auth import (authenticate, logout, views)
from django.contrib.auth.models import User
from django.forms.formsets import formset_factory
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.conf import settings
from django.http import Http404
import datetime
from mquiz.models import Quiz, Question, Response, QuizAttempt, QuizAttemptResponse
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


def browse(request, letter='A'):
    letters = []
    for i in range(0,26):
        char = chr(ord('A')+i)
        no_quizzes = Quiz.objects.filter(title__istartswith = char).count()
        letters.append([char,no_quizzes])
    quizzes = Quiz.objects.filter(title__istartswith = letter)
    return render(request, 'mquiz/browse.html', {'letters': letters, 'quizzes': quizzes })

# TODO? move these to separate reporting module?
def quiz_results_date(request,quiz_id):
    try:
        quiz = Quiz.objects.get(pk=quiz_id,draft=0,deleted=0)
    except Quiz.DoesNotExist:
        raise Http404
    dates = []
    startdate = datetime.datetime.now()
    for i in range(14,-1,-1):
        temp = startdate - datetime.timedelta(days=i)
        day = temp.strftime("%d")
        month = temp.strftime("%m")
        year = temp.strftime("%y")
        count = QuizAttempt.objects.filter(quiz=quiz,attempt_date__day=day,attempt_date__month=month,attempt_date__year=year).count()
        dates.append([temp.strftime("%d %b %y"),count])
    return render_to_response('mquiz/quiz/results/date.html',{'quiz':quiz, 'dates':dates }, context_instance=RequestContext(request))

def quiz_results_score(request,quiz_id):
    try:
        quiz = Quiz.objects.get(pk=quiz_id,draft=0,deleted=0)
    except Quiz.DoesNotExist:
        raise Http404
    attempts = QuizAttempt.objects.filter(quiz=quiz)
    data = {}
    for a in attempts:
        score = a.get_score_percent()
        if score in data:
            data[score] = data[score] + 1
        else:
            data[score] = 1
    return render_to_response('mquiz/quiz/results/score.html',{'quiz':quiz,'data':data }, context_instance=RequestContext(request))

def quiz_results_questions(request,quiz_id):
    # TODO - this could be done more efficiently?
    try:
        quiz = Quiz.objects.get(pk=quiz_id,draft=0,deleted=0)
    except Quiz.DoesNotExist:
        raise Http404
    questions = Question.objects.filter(quiz=quiz)
    data = {}
    for q in questions:
        maxscore = float(q.get_maxscore())
        responses = QuizAttemptResponse.objects.filter(question=q)
        maxtotal = 0
        usertotal = 0 
        for r in responses:
            maxtotal = maxtotal + maxscore
            usertotal = usertotal + float(r.score)
    
        if maxtotal > 0:
            data[q.title] = usertotal/maxtotal
        else:
            data[q.title] = 0

    return render_to_response('mquiz/quiz/results/questions.html',{'quiz':quiz,'data':data }, context_instance=RequestContext(request))

def quiz_results_attempts(request,quiz_id):
    try:
        # check current user is owner
        quiz = Quiz.objects.get(pk=quiz_id,owner=request.user)
    except Quiz.DoesNotExist:
        raise Http404
    attempts = QuizAttempt.objects.filter(quiz=quiz).order_by('-attempt_date')
    return render_to_response('mquiz/quiz/results/attempts.html',{'quiz':quiz,'attempts':attempts }, context_instance=RequestContext(request))

def my_results(request):
    results = QuizAttempt.objects.filter(user = request.user).order_by('-attempt_date')
    return render_to_response('mquiz/my_results.html', {'results': results}, context_instance=RequestContext(request))

def manage_view(request):
    pass
