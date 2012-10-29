#mquiz/api.py
from django.contrib.auth.models import User
from tastypie import fields
from tastypie.resources import ModelResource
from mquiz.models import Quiz,Question,Response


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'owner'

class QuizResource(ModelResource):
    owner = fields.ForeignKey(UserResource, 'owner')    
    class Meta:
        queryset = Quiz.objects.all()
        resource_name = 'quiz'
        
class QuestionResource(ModelResource):
    owner = fields.ForeignKey(UserResource, 'owner')    
    class Meta:
        queryset = Question.objects.all()
        resource_name = 'question'
        
class ResponseResource(ModelResource):
    owner = fields.ForeignKey(UserResource, 'owner')    
    class Meta:
        queryset = Response.objects.all()
        resource_name = 'response'
