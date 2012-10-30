# mquiz/api/resources.py
from django.contrib.auth.models import User
from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.authentication import BasicAuthentication
from mquiz.models import Quiz, Question, QuizQuestion, Response
from mquiz.api.auth import MquizAPIAuthorization
from mquiz.api.serializers import PrettyJSONSerializer


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['first_name', 'last_name', 'last_login','username']
        allowed_methods = ['get']
        authentication = BasicAuthentication()
        authorization= MquizAPIAuthorization() 
        serializer = PrettyJSONSerializer()
               
        
class QuizResource(ModelResource):
    class Meta:
        queryset = Quiz.objects.all()
        allowed_methods = ['get']
        fields = ['title', 'id']
        resource_name = 'quiz'
        serializer = PrettyJSONSerializer()
        
class QuizQuestionResource(ModelResource):
    quiz = fields.ToOneField('mquiz.api.resources.QuizResource', 'quiz', full=True)
    question = fields.ToOneField('mquiz.api.resources.QuestionResource', 'question', full=True)
    class Meta:
        queryset = QuizQuestion.objects.all()
        allowed_methods = ['get']
        resource_name = 'quiz/question'
        include_resource_uri = False
        serializer = PrettyJSONSerializer()
        
class QuestionResource(ModelResource):
    r = fields.ToManyField('mquiz.api.resources.ResponseResource', 'response_set', related_name='question', full=True)   
    class Meta:
        queryset = Question.objects.all()
        allowed_methods = ['get']
        fields = ['title']
        resource_name = 'question'
        include_resource_uri = False
        serializer = PrettyJSONSerializer()
        
class ResponseResource(ModelResource):
    class Meta:
        queryset = Response.objects.all()
        allowed_methods = ['get']
        fields = ['orderno', 'title','score']
        resource_name = 'response'
        include_resource_uri = False
        serializer = PrettyJSONSerializer()