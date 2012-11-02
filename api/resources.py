# mquiz/api/resources.py
from django.contrib.auth.models import User
from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.authentication import BasicAuthentication,Authentication
from tastypie.authorization import Authorization
from mquiz.models import Quiz, Question, QuizQuestion, Response, QuestionProps, QuizProps
from mquiz.api.auth import MquizAPIAuthorization
from mquiz.api.serializers import PrettyJSONSerializer, QuizJSONSerializer


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['first_name', 'last_name', 'last_login','username']
        allowed_methods = ['get']
        authentication = BasicAuthentication()
        authorization = MquizAPIAuthorization() 
        serializer = PrettyJSONSerializer()
               
        
class QuizResource(ModelResource):
    questions = fields.ToManyField('mquiz.api.resources.QuizQuestionResource', 'quizquestion_set', related_name='quiz', full=True)
    props = fields.ToManyField('mquiz.api.resources.QuizPropsResource', 'quizprops_set', related_name='quiz', full=True)
    owner = fields.ForeignKey(UserResource, 'owner')
    class Meta:
        queryset = Quiz.objects.filter(draft=0,deleted=0)
        allowed_methods = ['get','post']
        fields = ['title', 'id', 'description', 'lastupdated_date']
        resource_name = 'quiz'
        include_resource_uri = False
        serializer = QuizJSONSerializer()  
        authentication = BasicAuthentication()
        authorization = Authorization()
    
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
    responses = fields.ToManyField('mquiz.api.resources.ResponseResource', 'response_set', related_name='question', full=True)   
    props = fields.ToManyField('mquiz.api.resources.QuestionPropsResource', 'questionprops_set', related_name='question', full=True)
    owner = fields.ForeignKey(UserResource, 'owner')
    class Meta:
        queryset = Question.objects.all()
        allowed_methods = ['get','post']
        fields = ['title','type']
        resource_name = 'question'
        include_resource_uri = True
        serializer = PrettyJSONSerializer()
        authentication = BasicAuthentication()
        authorization = Authorization()
     
    #def obj_create(self, bundle, request=None, **kwargs):
    #    bundle = self.full_hydrate(bundle, request)
     #   return bundle

    #def obj_update(self, bundle, request=None, **kwargs):
    #    bundle = self.full_hydrate(bundle, request)
    #    return bundle
          
    #def full_hydrate(self, bundle, request=None):
    #    bundle = self.hydrate(bundle, request)
    #    return bundle
    
   # def hydrate(self, bundle, request=None):
        #bundle.obj.owner = User.objects.get(pk = request.user.id)
        #bundle.obj.owner = request.user.id
     #   return bundle
        
class ResponseResource(ModelResource):
    class Meta:
        queryset = Response.objects.all()
        allowed_methods = ['get','post']
        fields = ['id','question','order', 'title','score']
        resource_name = 'response'
        include_resource_uri = True
        serializer = PrettyJSONSerializer()
        authentication = BasicAuthentication()
        
class QuestionPropsResource(ModelResource):
    class Meta:
        queryset = QuestionProps.objects.all()
        allowed_methods = ['get']
        fields = ['name', 'value']
        resource_name = 'questionprop'
        include_resource_uri = False
        
class QuizPropsResource(ModelResource):
    class Meta:
        queryset = QuizProps.objects.all()
        allowed_methods = ['get']
        fields = ['name', 'value']
        resource_name = 'quizprop'
        include_resource_uri = False
        