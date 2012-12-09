# mquiz/reporting.py
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import (authenticate, logout, views)
from django.contrib.auth.models import User
from django.forms.formsets import formset_factory
from django.http import HttpResponseRedirect
from django.http import Http404
import datetime
from mquiz.models import Quiz, Question, Response, QuizAttempt, QuizAttemptResponse, QuizQuestion, QuestionProps, QuizProps
from django.utils.translation import ugettext as _

def quiz_results_date(request,quiz_id):
    try:
        quiz = Quiz.objects.get(pk=quiz_id,draft=0,deleted=0)
    except Quiz.DoesNotExist:
        raise Http404
    
    no_attempts = QuizAttempt.objects.filter(quiz=quiz).count()
    if no_attempts == 0:
         return render_to_response('mquiz/quiz/results/no_attempts.html',{'quiz':quiz}, context_instance=RequestContext(request))
    
    dates = []
    startdate = datetime.datetime.now()
    for i in range(31,-1,-1):
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
    if attempts.count() == 0:
         return render_to_response('mquiz/quiz/results/no_attempts.html',{'quiz':quiz}, context_instance=RequestContext(request))
    
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
    
    no_attempts = QuizAttempt.objects.filter(quiz=quiz).count()
    if no_attempts == 0:
         return render_to_response('mquiz/quiz/results/no_attempts.html',{'quiz':quiz}, context_instance=RequestContext(request))
    
    
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
    if attempts.count() == 0:
         return render_to_response('mquiz/quiz/results/no_attempts.html',{'quiz':quiz}, context_instance=RequestContext(request))
    
    for a in attempts:
        a.responses = QuizAttemptResponse.objects.filter(quizattempt=a)
    return render_to_response('mquiz/quiz/results/attempts.html',{'quiz':quiz,'attempts':attempts }, context_instance=RequestContext(request))

def my_results(request):
    results = QuizAttempt.objects.filter(user = request.user).order_by('-attempt_date')
    return render_to_response('mquiz/my_results.html', {'results': results}, context_instance=RequestContext(request))