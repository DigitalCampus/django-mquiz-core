# mquiz/api.py
from django.contrib.auth.models import User
from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.authentication import BasicAuthentication
from mquiz.models import Quiz
from mquiz.apiauth import MquizAPIAuthorization


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
        fields = ['title', 'id']
        resource_name = 'quiz'