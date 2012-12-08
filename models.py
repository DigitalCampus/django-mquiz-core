# mquiz/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core import serializers
from datetime import datetime
from tastypie.models import create_api_key

models.signals.post_save.connect(create_api_key, sender=User)

class Question(models.Model):
    QUESTION_TYPES = (
        ('multichoice', 'Multiple choice'),
        ('shortanswer', 'Short answer'),
        ('match', 'Matching'),
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
        percent = int(round(self.score * 100 / self.maxscore))
        return percent
    
class QuizAttemptResponse(models.Model):
    quizattempt = models.ForeignKey(QuizAttempt)
    question = models.ForeignKey(Question)
    score = models.DecimalField(decimal_places=2, max_digits=6)
    text = models.TextField(blank=True)
    
    def get_score_percent(self):
        percent = int(round(float(self.score) * 100 / self.question.get_maxscore()))
        return percent
    