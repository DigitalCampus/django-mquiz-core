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
from forms import QuizForm, QuestionForm, ResponseForm
from django.utils.translation import ugettext as _

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
    QuestionFormSet = formset_factory(QuestionForm, extra=3)
    
    if request.method == 'POST':
        quiz_form = QuizForm(request.POST)
        question_formset = QuestionFormSet(request.POST)
        
        if quiz_form.is_valid() and question_formset.is_valid():
            quiz = quiz_form.save(commit=False)
            quiz.lastupdated_date = datetime.datetime.now()
            quiz.owner = request.user
            quiz.save()
            process_quiz(request, quiz, question_formset)
            return HttpResponseRedirect('saved/')
    else:
        quiz_form = QuizForm() # An unbound form
        question_formset = QuestionFormSet()

    return render(request, 'mquiz/quiz/quiz.html', {'title': _(u"Create Quiz"), 'quiz_form': quiz_form,'question_formset':question_formset})

def edit_quiz(request,quiz_id):
    try:
        # check only the owner can edit
        quiz = Quiz.objects.get(pk=quiz_id,owner=request.user)
    except Quiz.DoesNotExist:
        raise Http404
    # TODO check a quiz can't be edited if already has attempts not by the owner
    # TODO don't allow editing of quizzes with digest props?
    QuestionFormSet = formset_factory(QuestionForm, extra=0)
    
    if request.method == 'POST':
        quiz_form = QuizForm(request.POST)
        question_formset = QuestionFormSet(request.POST)
        if quiz_form.is_valid() and question_formset.is_valid():
            quiz.title = quiz_form.cleaned_data.get("title").strip()
            quiz.description = quiz_form.cleaned_data.get("description").strip()
            quiz.save()
            
            # delete all quiz questions and props
            Question.objects.filter(quiz=quiz).delete()
            QuizProps.objects.filter(quiz=quiz).delete()
            
            process_quiz(request,quiz,question_formset)
            return HttpResponseRedirect('saved/')
    else:
        quiz_form = QuizForm(initial={'title':quiz.title,
                                    'description':quiz.description})
        initial = []
        questions = Question.objects.filter(quiz=quiz)
        for q in questions:
            data = {}
            data['title'] = q.title
            data['type'] = q.type
            responses = Response.objects.filter(question=q)
            for idx, r in enumerate(responses):
                data['response'+str(idx+1)] = r.title
                data['score'+str(idx+1)] = r.score
            initial.append(data)
        question_formset = QuestionFormSet(initial=initial)

    return render(request, 'mquiz/quiz/quiz.html', {'title': _(u"Edit Quiz"), 'quiz_form': quiz_form,'question_formset':question_formset})

def delete_quiz(request,quiz_id):
    pass

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

def manage_view(request):
    quizzes = Quiz.objects.filter(owner=request.user).order_by('title')
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

def process_quiz(request,quiz,question_formset):
    
    quiz_maxscore = 0
    
    for idx, question_form in enumerate(question_formset):
        
        # add each question and response
        title = question_form.cleaned_data.get("title").strip()
        type = question_form.cleaned_data.get("type").strip()
        question = Question()
        question.title = title
        question.type = type
        question.owner = request.user
        question.save()
        
        question_maxscore = 0
        # add responses
        needs_answers = True
        if type == 'essay' or type=='info':
            needs_answers = False
        
        if needs_answers:
            for i in range(1,4):
                response = question_form.cleaned_data.get("response"+str(i)).strip()
                rscore = question_form.cleaned_data.get("score"+str(i))
                if response != "":
                    # TODO checks based on question type
                    # if numerical then split on tolerance
                    r = Response()
                    r.owner = request.user
                    r.question = question
                    r.score = rscore
                    r.title = response
                    r.order = i
                    r.save()
                    question_maxscore = question_maxscore + rscore
                    
        # add maxscore for question
        qp = QuestionProps()
        qp.question = question
        qp.name = 'maxscore'
        qp.value = question_maxscore
        qp.save()
        
        quiz_maxscore = quiz_maxscore + question_maxscore
        
        # add question to quiz
        quizquestion = QuizQuestion()
        quizquestion.quiz = quiz
        quizquestion.question = question
        quizquestion.order = idx+1
        quizquestion.save()                 
    
    return
