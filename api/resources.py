# mquiz_api/resources.py
from django.contrib.auth.models import User
from tastypie import fields, bundle
from tastypie.resources import ModelResource
from tastypie.authentication import BasicAuthentication,Authentication
from tastypie.authorization import Authorization
from tastypie import http
from tastypie.exceptions import NotFound, BadRequest, InvalidFilterError, HydrationError, InvalidSortError, ImmediateHttpResponse
from mquiz.models import Quiz, Question, QuizQuestion, Response, QuestionProps, QuizProps, ResponseProps
from mquiz.api.auth import MquizAPIAuthorization
from mquiz.api.serializers import PrettyJSONSerializer, QuizJSONSerializer
from tastypie.validation import Validation


class QuizOwnerValidation(Validation):
    def is_valid(self, bundle, request=None):
        if not bundle.data:
            return {'__all__': 'no data.'}
        errors = {}
        quiz = QuizResource().get_via_uri(bundle.data['quiz'])
        if quiz.owner.id != bundle.request.user.id:
            errors['error_message'] = "You are not the owner of this quiz"
        return errors
    
class QuestionOwnerValidation(Validation):
    def is_valid(self, bundle, request=None):
        if not bundle.data:
            return {'__all__': 'no data.'}
        errors = {}
        question = QuestionResource().get_via_uri(bundle.data['question'])
        if question.owner.id != bundle.request.user.id:
            errors['error_message'] = "You are not the owner of this question"
        return errors
    
class ResponseOwnerValidation(Validation):
    def is_valid(self, bundle, request=None):
        if not bundle.data:
            return {'__all__': 'no data.'}
        errors = {}
        response = ResponseResource().get_via_uri(bundle.data['response'])
        if response.owner.id != bundle.request.user.id:
            errors['error_message'] = "You are not the owner of this response"
        return errors 
   
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
        include_resource_uri = True
        serializer = QuizJSONSerializer()  
        authentication = BasicAuthentication()
        authorization = Authorization()
        always_return_data = True
        
    def hydrate(self, bundle, request=None):
        bundle.obj.owner = User.objects.get(pk = bundle.request.user.id)
        return bundle 
    
class QuizQuestionResource(ModelResource):
    #quiz = fields.ToOneField('mquiz_api.resources.QuizResource', 'quiz', full=True)
    question = fields.ToOneField('mquiz.api.resources.QuestionResource', 'question', full=True)
    class Meta:
        queryset = QuizQuestion.objects.all()
        allowed_methods = ['get','post']
        fields = ['id','order','question']
        include_resource_uri = True
        authentication = BasicAuthentication()
        authorization = Authorization()
        validation = QuizOwnerValidation()
        always_return_data = True
      
    def hydrate(self, bundle, request=None):
        bundle.obj.quiz_id = QuizResource().get_via_uri(bundle.data['quiz']).id
        return bundle
     
class QuestionResource(ModelResource):
    #quiz = fields.ToManyField('mquiz_api.resources.QuizQuestionResource', 'quiz', full=True)
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
        always_return_data = True

    def hydrate(self, bundle, request=None):
        bundle.obj.owner = User.objects.get(pk = bundle.request.user.id)
        return bundle   
    
class ResponseResource(ModelResource):
    question = fields.ForeignKey(QuestionResource, 'question')
    props = fields.ToManyField('mquiz.api.resources.ResponsePropsResource', 'responseprops_set', related_name='response', full=True)
    class Meta:
        queryset = Response.objects.all()
        allowed_methods = ['get','post']
        fields = ['id','order', 'title','score']
        resource_name = 'response'
        include_resource_uri = True
        serializer = PrettyJSONSerializer()
        authentication = BasicAuthentication()
        authorization = Authorization()
        validation = QuestionOwnerValidation()
        always_return_data = True
        
    def hydrate(self, bundle, request=None):
        bundle.obj.owner = User.objects.get(pk = bundle.request.user.id)
        return bundle 
        
class QuestionPropsResource(ModelResource):
    question = fields.ForeignKey(QuestionResource, 'question')
    class Meta:
        queryset = QuestionProps.objects.all()
        allowed_methods = ['get','post']
        fields = ['name', 'value']
        resource_name = 'questionprops'
        include_resource_uri = False
        authentication = BasicAuthentication()  
        authorization = Authorization()
        validation = QuestionOwnerValidation()
        always_return_data = True
           
class QuizPropsResource(ModelResource):
    quiz = fields.ForeignKey(QuizResource, 'quiz')
    class Meta:
        queryset = QuizProps.objects.all()
        allowed_methods = ['get','post']
        fields = ['name', 'value']
        resource_name = 'quizprops'
        include_resource_uri = False
        authentication = BasicAuthentication()  
        authorization = Authorization()
        validation = QuizOwnerValidation()
        always_return_data = True
   
class ResponsePropsResource(ModelResource):
    response = fields.ForeignKey(ResponseResource, 'response')
    class Meta:
        queryset = ResponseProps.objects.all()
        allowed_methods = ['get','post']
        fields = ['name', 'value']
        resource_name = 'responseprops'
        include_resource_uri = False
        authentication = BasicAuthentication()  
        authorization = Authorization()
        validation = ResponseOwnerValidation()
        always_return_data = True     

class RegisterResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'register'
        fields = ['first_name', 'last_name', 'last_login','username']
        allowed_methods = ['post']
        #authentication = Authentication()
        authorization = Authorization() 
        serializer = PrettyJSONSerializer()  
        always_return_data = True     
