# mquiz/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core import serializers
from datetime import datetime
from tastypie.models import create_api_key
from badges.receivers import quizattempt_callback, createquiz_callback, signup_callback

models.signals.post_save.connect(create_api_key, sender=User)
models.signals.post_save.connect(signup_callback, sender=User)

class Question(models.Model):
    QUESTION_TYPES = (
        ('multichoice', 'Multiple choice'),
        ('shortanswer', 'Short answer'),
        ('matching', 'Matching'),
        ('numerical', 'Numerical'),
        ('essay', 'Essay'),
        ('multiselect', 'Multiple select'),
        ('info', 'Information only'),
    )
    owner = models.ForeignKey(User)
    created_date = models.DateTimeField('date created',default=datetime.now)
    lastupdated_date = models.DateTimeField('date updated',default=datetime.now)
    title = models.TextField(blank=False)  
    type = models.CharField(max_length=15,choices=QUESTION_TYPES, default='multichoice') 
    def __unicode__(self):
        return self.title
    
    def get_maxscore(self):
        props = QuestionProps.objects.get(question=self,name='maxscore')
        return float(props.value);

class Response(models.Model):
    owner = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    created_date = models.DateTimeField('date created',default=datetime.now)
    lastupdated_date = models.DateTimeField('date updated',default=datetime.now)
    score = models.DecimalField(default=0,decimal_places=2, max_digits=6)
    title = models.TextField(blank=False)
    order = models.IntegerField(default=1)
    def __unicode__(self):
        return self.title
    
class Quiz(models.Model):
    owner = models.ForeignKey(User)
    created_date = models.DateTimeField('date created',default=datetime.now)
    lastupdated_date = models.DateTimeField('date updated',default=datetime.now)
    draft = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    title = models.TextField(blank=False)
    description = models.TextField(blank=True)
    questions = models.ManyToManyField(Question, through='QuizQuestion')
    
    def __unicode__(self):
        return self.title
    
class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz)
    question = models.ForeignKey(Question)
    order = models.IntegerField(default=1)

class QuizProps(models.Model):
    quiz = models.ForeignKey(Quiz)
    name = models.CharField(max_length=200)
    value = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.name
    
class QuestionProps(models.Model):
    question = models.ForeignKey(Question)
    name = models.CharField(max_length=200)
    value = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.name
    
class ResponseProps(models.Model):
    response = models.ForeignKey(Response)
    name = models.CharField(max_length=200)
    value = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.name
    
class QuizAttempt(models.Model):
    user = models.ForeignKey(User)
    quiz = models.ForeignKey(Quiz)
    attempt_date = models.DateTimeField('date attempted',default=datetime.now)
    submitted_date = models.DateTimeField('date submitted',default=datetime.now)
    score = models.DecimalField(decimal_places=2, max_digits=6)
    maxscore = models.DecimalField(decimal_places=2, max_digits=6)
    ip = models.IPAddressField()
    agent = models.TextField(blank=True)
    
    def get_score_percent(self):
        if self.maxscore > 0:
            percent = int(round(self.score * 100 / self.maxscore))
        else:
            percent = 0
        return percent
    
    def is_first_attempt(self,user):
        no_attempts = QuizAttempt.objects.filter(user=user,quiz=self.quiz).count()
        is_first_attempt = False
        if no_attempts == 1:
            is_first_attempt = True
        return is_first_attempt
    
    def is_first_attempt_today(self,user):
        date = datetime.now()
        day = date.strftime("%d")
        month = date.strftime("%m")
        year = date.strftime("%y")
        no_attempts_today = QuizAttempt.objects.filter(user=user,quiz=self.quiz,submitted_date__day=day,submitted_date__month=month,submitted_date__year=year).count()
        is_first_attempt_today = False
        if no_attempts_today == 1:
            is_first_attempt_today = True
        return is_first_attempt_today
        
class QuizAttemptResponse(models.Model):
    quizattempt = models.ForeignKey(QuizAttempt)
    question = models.ForeignKey(Question)
    score = models.DecimalField(decimal_places=2, max_digits=6)
    text = models.TextField(blank=True)
    
    def get_score_percent(self):
        if self.question.get_maxscore() > 0:
            percent = int(round(float(self.score) * 100 / self.question.get_maxscore()))
        else:
            percent = 0
        return percent
  
models.signals.post_save.connect(createquiz_callback, sender=Quiz)
models.signals.post_save.connect(quizattempt_callback, sender=QuizAttempt)