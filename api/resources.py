# mquiz/api/resources.py
from django.contrib.auth.models import User
from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.authentication import BasicAuthentication
from mquiz.models import Quiz, Question, QuizQuestion, Response
from mquiz.api.auth import MquizAPIAuthorization
from mquiz.api.serializers import PrettyJSONSerializer, QuizJSONSerializer


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
    q = fields.ToManyField('mquiz.api.resources.QuizQuestionResource', 'quizquestion_set', related_name='quiz', full=True)
    class Meta:
        queryset = Quiz.objects.all()
        allowed_methods = ['get']
        fields = ['title', 'id', 'description']
        resource_name = 'quiz'
        include_resource_uri = False
        serializer = QuizJSONSerializer()   
    
class QuizQuestionResource(ModelResource):
    #quiz = fields.ToOneField('mquiz.api.resources.QuizResource', 'quiz', full=True)
    question = fields.ToOneField('mquiz.api.resources.QuestionResource', 'question', full=True)
    class Meta:
        queryset = QuizQuestion.objects.all()
        allowed_methods = ['get']
        fields = ['id','order']
        include_resource_uri = False
      
class QuestionResource(ModelResource):
    #quiz = fields.ToManyField('mquiz.api.resources.QuizQuestionResource', 'quiz', full=True)
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