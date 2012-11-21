# mquiz/api/resources.py
# TODO - tidy these imports
from django.contrib.auth.models import User
from django.contrib.auth import (authenticate, login)
from tastypie import fields, bundle
from tastypie.resources import ModelResource
from tastypie.authentication import Authentication, ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie import http
from tastypie.exceptions import NotFound, BadRequest, InvalidFilterError, HydrationError, InvalidSortError, ImmediateHttpResponse
from mquiz.models import Quiz, Question, QuizQuestion, Response, QuestionProps, QuizProps, ResponseProps, QuizAttempt, QuizAttemptResponse
from mquiz.api.auth import MquizAPIAuthorization
from mquiz.api.serializers import PrettyJSONSerializer, QuizJSONSerializer, UserJSONSerializer
from tastypie.validation import Validation
from django.db import IntegrityError
from tastypie.models import ApiKey

class QuizOwnerValidation(Validation):
    def is_valid(self, bundle, request=None):
        if not bundle.data:
            return {'__all__': 'no data.'}
        errors = {}
        quiz = QuizResource().get_via_uri(bundle.data['quiz'])
        if quiz.owner.id != bundle.request.user.id:
            # TODO translation
            errors['error_message'] = "You are not the owner of this quiz"
        return errors
    
class QuestionOwnerValidation(Validation):
    def is_valid(self, bundle, request=None):
        if not bundle.data:
            return {'__all__': 'no data.'}
        errors = {}
        question = QuestionResource().get_via_uri(bundle.data['question'])
        if question.owner.id != bundle.request.user.id:
            # TODO translation
            errors['error_message'] = "You are not the owner of this question"
        return errors
    
class ResponseOwnerValidation(Validation):
    def is_valid(self, bundle, request=None):
        if not bundle.data:
            return {'__all__': 'no data.'}
        errors = {}
        response = ResponseResource().get_via_uri(bundle.data['response'])
        if response.owner.id != bundle.request.user.id:
            # TODO translation
            errors['error_message'] = "You are not the owner of this response"
        return errors 
   
class UserResource(ModelResource):
    #api_key = fields.ToOneField('mquiz.api.resources.QuestionResource', 'user', full=True)
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['first_name', 'last_name', 'last_login','username']
        allowed_methods = ['post']
        authentication = Authentication()
        authorization = Authorization() 
        serializer = UserJSONSerializer()
        always_return_data = True       
    
    def obj_create(self, bundle, request=None, **kwargs):
        username = bundle.data['username']
        password = bundle.data['password']
        if not username or not password:
            raise BadRequest('Username or password missing')
        
        u = authenticate(username=username, password=password)
        if u is not None:
            if u.is_active:
                login(request, u)
            else:
                # TODO - should raise 401 error
                raise BadRequest('Authentication failure')
        else:
            # TODO should raise 401 error
            raise BadRequest('Authentication failure')

        # TODO Change to delete key (remove completely, not just empty
        bundle.data['password'] = ''
        key = ApiKey.objects.get(user = u)
        bundle.data['api_key'] = key.key
        bundle.obj = u
        return bundle 
        
          
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
        authentication = ApiKeyAuthentication()
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
        include_resource_uri = False
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        validation = QuizOwnerValidation()
        always_return_data = True
      
    def hydrate(self, bundle, request=None):
        bundle.obj.quiz_id = QuizResource().get_via_uri(bundle.data['quiz']).id
        return bundle
     
class QuestionResource(ModelResource):
    responses = fields.ToManyField('mquiz.api.resources.ResponseResource', 'response_set', related_name='question', full=True)   
    props = fields.ToManyField('mquiz.api.resources.QuestionPropsResource', 'questionprops_set', related_name='question', full=True, null=True)
    owner = fields.ForeignKey(UserResource, 'owner')
    class Meta:
        queryset = Question.objects.all()
        allowed_methods = ['get','post']
        fields = ['title','type']
        resource_name = 'question'
        include_resource_uri = True
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        # TODO - format better to show responses/props as in QuizResource
        always_return_data = True

    def hydrate(self, bundle, request=None):
        bundle.obj.owner = User.objects.get(pk = bundle.request.user.id)
        return bundle   
 
class QuestionPropsResource(ModelResource):
    question = fields.ToOneField('mquiz.api.resources.QuestionResource', 'question', related_name='questionprops')
    class Meta:
        queryset = QuestionProps.objects.all()
        allowed_methods = ['get','post']
        fields = ['name', 'value']
        # TODO how to put slash in the name?
        resource_name = 'questionprops'
        include_resource_uri = False
        authentication = ApiKeyAuthentication()  
        authorization = Authorization()
        validation = QuestionOwnerValidation()
        always_return_data = True
 
    
class ResponseResource(ModelResource):
    question = fields.ForeignKey(QuestionResource, 'question')
    props = fields.ToManyField('mquiz.api.resources.ResponsePropsResource', 'responseprops_set', related_name='response', full=True, null=True)
    class Meta:
        queryset = Response.objects.all()
        allowed_methods = ['get','post']
        fields = ['id','order', 'title','score']
        resource_name = 'response'
        include_resource_uri = False
        serializer = PrettyJSONSerializer()
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        validation = QuestionOwnerValidation()
        always_return_data = True
        
    def hydrate(self, bundle, request=None):
        bundle.obj.owner = User.objects.get(pk = bundle.request.user.id)
        return bundle 
 
class ResponsePropsResource(ModelResource):
    response = fields.ToOneField('mquiz.api.resources.ResponseResource', 'response', related_name='responseprops')
    class Meta:
        queryset = ResponseProps.objects.all()
        allowed_methods = ['get','post']
        fields = ['name', 'value']
        # TODO how to put slash in the name?
        resource_name = 'responseprops'
        include_resource_uri = False
        authentication = ApiKeyAuthentication()  
        authorization = Authorization()
        validation = ResponseOwnerValidation()
        always_return_data = True            

           
class QuizPropsResource(ModelResource):
    quiz = fields.ForeignKey(QuizResource, 'quiz')
    class Meta:
        queryset = QuizProps.objects.all()
        allowed_methods = ['get','post']
        fields = ['name', 'value']
        # TODO how to put slash in the name?
        resource_name = 'quizprops'
        include_resource_uri = False
        authentication = ApiKeyAuthentication()  
        authorization = Authorization()
        validation = QuizOwnerValidation()
        always_return_data = True
   



class RegisterResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'register'
        allowed_methods = ['post']
        authorization = Authorization() 
        always_return_data = False 
         
    def obj_create(self, bundle, request=None, **kwargs):
        # TODO - must be a better way to do this...
        try:
            username = bundle.data['username']
        except KeyError:
            # TODO translation
            raise BadRequest('Please supply a username')
        try:
            password = bundle.data['password']
        except KeyError:
            # TODO translation
            raise BadRequest('Please supply a password')
        try:
            password_again = bundle.data['passwordagain']
        except KeyError:
            # TODO translation
            raise BadRequest('Please supply a password again')
        try:
            email = bundle.data['email']
        except KeyError:
            # TODO translation
            raise BadRequest('Please supply an email')
        try:
            first_name = bundle.data['firstname']
        except KeyError:
            # TODO translation
            raise BadRequest('Please supply a first name')  
        try:
            last_name = bundle.data['lastname']
        except KeyError:
            # TODO translation
            raise BadRequest('Please supply a last name') 
        # TODO check firstname and lastname longer than 2
        # TODO check valid email address
        # TODO check passwords match
        # TODO check password longer than 6
        try:
            bundle.obj = User.objects.create_user(username, email, password)
            bundle.obj.first_name = first_name
            bundle.obj.last_name = last_name
            bundle.obj.save()
            u = authenticate(username=username, password=password)
            if u is not None:
                if u.is_active:
                    login(bundle.request, u)
        except IntegrityError:
            # TODO translation
            raise BadRequest('That username already exists')
        return bundle   
 
class QuizAttemptResponseResource(ModelResource):
    question = fields.ForeignKey(QuestionResource, 'question')
    quizattempt = fields.ToOneField('mquiz.api.resources.QuizAttemptResource', 'quizattempt', related_name='quizattemptresponse')
    class Meta:
        queryset = QuizAttemptResponse.objects.all()
        # TODO - better name?
        # TODO how to put slash in the name?
        resource_name = 'quizattemptresponse'
        allowed_methods = ['post']
        authentication = ApiKeyAuthentication()
        authorization = Authorization()    
           
class QuizAttemptResource(ModelResource):
    quiz = fields.ForeignKey(QuizResource, 'quiz')
    user = fields.ForeignKey(UserResource, 'user')
    responses = fields.ToManyField('mquiz.api.resources.QuizAttemptResponseResource', 'quizattemptresponse_set', related_name='quizattempt', full=True, null=True)
    class Meta:
        queryset = QuizAttempt.objects.all()
        resource_name = 'quizattempt'
        allowed_methods = ['post']
        authentication = ApiKeyAuthentication()
        authorization = Authorization() 
         
    def hydrate(self, bundle, request=None):
        # TODO - as extra check - check if the 'sent' param is false
        bundle.obj.user = User.objects.get(pk = bundle.request.user.id)
        bundle.data['quiz'] = Quiz.objects.get(pk = bundle.data['quiz_id'])
        # get the question resource uri from the question id
        for response in bundle.data['responses']:
            # TODO should check that the question is actually in this quiz first
            response['question'] = Question.objects.get(pk = response['question_id'])
        return bundle 
    