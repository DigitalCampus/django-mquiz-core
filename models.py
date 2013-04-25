# mquiz/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core import serializers
from tastypie.models import create_api_key
from badges.signals import signup_callback, createquiz_callback, quizattempt_callback
import datetime

models.signals.post_save.connect(create_api_key, sender=User)
models.signals.post_save.connect(signup_callback, sender=User)

class Question(models.Model):
    QUESTION_TYPES = (
        ('multichoice', 'Multiple choice'),
        ('shortanswer', 'Short answer'),
        ('matching', 'Matching'),
        ('numerical', 'Numerical'),
        ('multiselect', 'Multiple select'),
        ('info', 'Information only'),
    )
    owner = models.ForeignKey(User)
    created_date = models.DateTimeField('date created',default=datetime.datetime.now)
    lastupdated_date = models.DateTimeField('date updated',default=datetime.datetime.now)
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
    created_date = models.DateTimeField('date created',default=datetime.datetime.now)
    lastupdated_date = models.DateTimeField('date updated',default=datetime.datetime.now)
    score = models.DecimalField(default=0,decimal_places=2, max_digits=6)
    title = models.TextField(blank=False)
    order = models.IntegerField(default=1)
    def __unicode__(self):
        return self.title
    
class Quiz(models.Model):
    owner = models.ForeignKey(User)
    created_date = models.DateTimeField('date created',default=datetime.datetime.now)
    lastupdated_date = models.DateTimeField('date updated',default=datetime.datetime.now)
    draft = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    title = models.TextField(blank=False)
    description = models.TextField(blank=True)
    questions = models.ManyToManyField(Question, through='QuizQuestion')
    
    def __unicode__(self):
        return self.title
    
    def no_attempts(self):
        no_attempts = QuizAttempt.objects.filter(quiz=self).count()
        return no_attempts
    
    def avg_score(self):
        # TODO - sure this could be tidied up
        attempts = QuizAttempt.objects.filter(quiz=self)
        total = 0
        for a in attempts:
            total = total + a.get_score_percent()
        if self.no_attempts > 0:
            avg_score = int(total/self.no_attempts())
        else:
            avg_score = 0
        return avg_score
    
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
    attempt_date = models.DateTimeField('date attempted',default=datetime.datetime.now)
    submitted_date = models.DateTimeField('date submitted',default=datetime.datetime.now)
    score = models.DecimalField(decimal_places=2, max_digits=6)
    maxscore = models.DecimalField(decimal_places=2, max_digits=6)
    ip = models.IPAddressField()
    instance_id = models.CharField(max_length=50,null=True,blank=True)
    agent = models.TextField(blank=True)
    
    def get_score_percent(self):
        if self.maxscore > 0:
            percent = int(round(self.score * 100 / self.maxscore))
        else:
            percent = 0
        return percent
    
    def is_first_attempt(self):
        no_attempts = QuizAttempt.objects.filter(user=self.user,quiz=self.quiz).count()
        if no_attempts == 1:
            return True
        else:
            return False
    
    def is_first_attempt_today(self):    
        olddate = datetime.datetime.now() + datetime.timedelta(hours=-24)
        no_attempts_today = QuizAttempt.objects.filter(user=self.user,quiz=self.quiz,submitted_date__gte=olddate).count()
        if no_attempts_today == 1:
            return True
        else:
            return False
        
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