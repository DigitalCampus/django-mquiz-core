#mquiz/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core import serializers
from datetime import datetime

class Question(models.Model):
    owner = models.ForeignKey(User)
    created_date = models.DateTimeField('date created',default=datetime.now)
    lastupdated_date = models.DateTimeField('date updated',default=datetime.now)
    title = models.CharField(max_length=500)
    
    def __unicode__(self):
        return self.title
    def max_score(self):
        return 0

class Response(models.Model):
    owner = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    created_date = models.DateTimeField('date created',default=datetime.now)
    lastupdated_date = models.DateTimeField('date updated',default=datetime.now)
    score = models.IntegerField(default=0)
    title = models.CharField(max_length=200)
    orderno = models.IntegerField(default=1)
    def __unicode__(self):
        return self.title
    
class Quiz(models.Model):
    owner = models.ForeignKey(User)
    created_date = models.DateTimeField('date created',default=datetime.now)
    lastupdated_date = models.DateTimeField('date updated',default=datetime.now)
    draft = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    props = models.TextField(blank=True)
    questions = models.ManyToManyField(Question, through='QuizQuestion')
    
    def __unicode__(self):
        return self.title
    def max_score(self):
        return 0
    
class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz)
    question = models.ForeignKey(Question)
    order = models.IntegerField(default=1)

