# mquiz/quiz/quiz.py
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
from mquiz.forms import QuizForm, QuestionForm, BaseQuestionFormSet
from django.utils.translation import ugettext as _

def create_quiz(request):
    QuestionFormSet = formset_factory(QuestionForm, extra=3, formset=BaseQuestionFormSet)
    
    if request.method == 'POST':
        quiz_form = QuizForm(request.POST)
        question_formset = QuestionFormSet(request.POST)
        
        if quiz_form.is_valid() and question_formset.is_valid():
            quiz = quiz_form.save(commit=False)
            quiz.lastupdated_date = datetime.datetime.now()
            quiz.owner = request.user
            quiz.save()
            process_quiz(request, quiz, question_formset)
            return HttpResponseRedirect('../%d/saved/' % quiz.id)
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
    QuestionFormSet = formset_factory(QuestionForm, extra=0, formset=BaseQuestionFormSet)
    
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
            return HttpResponseRedirect('../saved/')
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

def saved_quiz(request, quiz_id):
    try:
        # check only the owner can edit
        quiz = Quiz.objects.get(pk=quiz_id,owner=request.user)
    except Quiz.DoesNotExist:
        raise Http404
    return render_to_response('mquiz/quiz/saved.html', 
                                  {'quiz': quiz},
                                  context_instance=RequestContext(request))
    
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
        if type == 'essay':
            question_maxscore = 1
            
        if needs_answers:
            for i in range(1,4):
                response = question_form.cleaned_data.get("response"+str(i)).strip()
                rscore = question_form.cleaned_data.get("score"+str(i))
                if response != "":
                    # TODO question type processing (for numerical questions only really)
                    # if numerical then split on tolerance
                    r = Response()
                    r.owner = request.user
                    r.question = question
                    r.score = rscore
                    r.title = response
                    r.order = i
                    r.save()
                    # check maxscore for shortanswer/numerical questions where there may be more than one score, but only 1 should be the max
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
