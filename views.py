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
from mquiz.models import Quiz, Question, Response, QuizAttempt, QuizAttemptResponse, QuizQuestion, QuestionProps, QuizProps
from forms import QuizForm, QuestionForm, BaseQuestionFormSet
from django.utils.translation import ugettext as _
from django.db.models import Count

def home_view(request):
    latest_quiz_list = Quiz.objects.filter(draft=0,deleted=0).order_by('-created_date')[:10]
    popular_quiz_list = Quiz.objects.filter(draft=0,deleted=0).annotate(num_attempts=Count('quizattempt')).order_by('-num_attempts')[:10]
    leaderboard = User.objects.raw("SELECT count( id ) AS no_attempts, user_id as id, AVG( (score *100 / maxscore) ) AS score_percent FROM mquiz_quizattempt WHERE maxscore !=0 GROUP BY user_id HAVING count( id ) >3 ORDER BY score_percent DESC LIMIT 0 , 10")
    return render_to_response('mquiz/home.html',
                              {'latest_quiz_list': latest_quiz_list,
                               'popular_quiz_list':popular_quiz_list,
                               'leaderboard': leaderboard,}, 
                              context_instance=RequestContext(request))

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
                     
def browse(request, letter='A'):
    letters = []
    for i in range(0,26):
        char = chr(ord('A')+i)
        no_quizzes = Quiz.objects.filter(draft=0, deleted=0,title__istartswith = char).count()
        letters.append([char,no_quizzes])
    quizzes = Quiz.objects.filter(draft=0, deleted=0,title__istartswith = letter).order_by('title')
    return render(request, 'mquiz/browse.html', {'letters': letters, 'quizzes': quizzes })

def manage_view(request):
    quizzes = Quiz.objects.filter(owner=request.user,deleted=0).order_by('title')
    for q in quizzes:
        attempts = QuizAttempt.objects.filter(quiz=q)
        q.no_attempts = attempts.count()
        total = 0
        for a in attempts:
            total = total + a.get_score_percent()
        if q.no_attempts > 0:
            q.avg_score = int(total/q.no_attempts)
        else:
            q.avg_score = 0
    return render_to_response('mquiz/manage.html',{'quizzes':quizzes}, context_instance=RequestContext(request))

