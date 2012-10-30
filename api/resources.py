# mquiz/api/resources.py
from django.contrib.auth.models import User
from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.authentication import BasicAuthentication
from mquiz.models import Quiz, Question, QuizQuestion, Response
from mquiz.api.auth import MquizAPIAuthorization


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['first_name', 'last_name', 'last_login','username']
        allowed_methods = ['get']
        authentication = BasicAuthentication()
        authorization= MquizAPIAuthorization()        
        
class QuizResource(ModelResource):
    class Meta:
        queryset = Quiz.objects.all()
        allowed_methods = ['get']
        fields = ['title', 'id']
        resource_name = 'quiz'
        
class QuizQuestionResource(ModelResource):
    class Meta:
        queryset = Question.objects.all()
        allowed_methods = ['get']
        resource_name = 'quiz/question'
        
class QuestionResource(ModelResource):
    responses = fields.ToManyField('mquiz.api.ResponseResource', 'responses')    
    class Meta:
        queryset = Question.objects.all()
        allowed_methods = ['get']
        resource_name = 'question'
        
class ResponseResource(ModelResource):
    question = fields.ToOneField(QuestionResource, 'question')
    class Meta:
        queryset = Response.objects.all()
        allowed_methods = ['get']
        resource_name = 'response'