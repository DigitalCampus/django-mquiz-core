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
from badges.models import Points
from django.core.paginator import Paginator, InvalidPage, EmptyPage

def home_view(request):
    latest_quiz_list = Quiz.objects.filter(draft=0,deleted=0).order_by('-created_date')[:10]
    popular_quiz_list = Quiz.objects.filter(draft=0,deleted=0).annotate(num_attempts=Count('quizattempt')).order_by('-num_attempts')[:10]
    leaderboard = Points.get_leaderboard(20)
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
    qzs = Quiz.objects.filter(owner=request.user,deleted=0).order_by('title')
    paginator = Paginator(qzs, 25) # Show 25 contacts per page

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        quizzes = paginator.page(page)
    except (EmptyPage, InvalidPage):
        quizzes = paginator.page(paginator.num_pages)
    return render_to_response('mquiz/manage.html',{'page':quizzes}, context_instance=RequestContext(request))

def scoreboard_view(request):
    lb = Points.get_leaderboard()
    paginator = Paginator(lb, 25) # Show 25 contacts per page

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
        leaderboard = paginator.page(page)
    except (EmptyPage, InvalidPage):
        leaderboard = paginator.page(paginator.num_pages)

    return render_to_response('mquiz/scoreboard.html',{'page':leaderboard}, context_instance=RequestContext(request))