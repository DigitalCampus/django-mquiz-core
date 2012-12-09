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
from mquiz.profile.forms import RegisterForm
from django.conf.urls.defaults import url
from django.core.paginator import Paginator, InvalidPage
from django.db.models import Q
from django.utils.translation import ugettext as _

class QuizOwnerValidation(Validation):
    def is_valid(self, bundle, request=None):
        if not bundle.data:
            return {'__all__': 'no data.'}
        errors = {}
        quiz = QuizResource().get_via_uri(bundle.data['quiz'])
        if quiz.owner.id != bundle.request.user.id:
            errors['error_message'] = _(u"You are not the owner of this quiz")
        return errors
    
class QuestionOwnerValidation(Validation):
    def is_valid(self, bundle, request=None):
        if not bundle.data:
            return {'__all__': 'no data.'}
        errors = {}
        question = QuestionResource().get_via_uri(bundle.data['question'])
        if question.owner.id != bundle.request.user.id:
            errors['error_message'] = _(u"You are not the owner of this question")
        return errors
    
class ResponseOwnerValidation(Validation):
    def is_valid(self, bundle, request=None):
        if not bundle.data:
            return {'__all__': 'no data.'}
        errors = {}
        response = ResponseResource().get_via_uri(bundle.data['response'])
        if response.owner.id != bundle.request.user.id:
            errors['error_message'] = _(u"You are not the owner of this response")
        return errors 
   
class UserResource(ModelResource):
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
            raise BadRequest(_(u'Username or password missing'))
        
        u = authenticate(username=username, password=password)
        if u is not None:
            if u.is_active:
                login(request, u)
            else:
                # TODO - should raise 401 error
                raise BadRequest(_(u'Authentication failure'))
        else:
            # TODO should raise 401 error
            raise BadRequest(_(u'Authentication failure'))

        del bundle.data['password']
        key = ApiKey.objects.get(user = u)
        bundle.data['api_key'] = key.key
        bundle.obj = u
        return bundle 
        
          
class QuizResource(ModelResource):
    questions = fields.ToManyField('mquiz.api.resources.QuizQuestionResource', 'quizquestion_set', related_name='quiz', full=True)
    props = fields.ToManyField('mquiz.api.resources.QuizPropsResource', 'quizprops_set', related_name='quiz', full=True)
    owner = fields.ForeignKey(UserResource, 'owner')
    class Meta:
        queryset = Quiz.objects.filter(draft=0,deleted=0).order_by('-lastupdated_date')
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
    
    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search/$" % self._meta.resource_name, self.wrap_view('get_search'), name="api_get_search"),
        ]
        
    def get_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        # Do the query.
        #sqs = SearchQuerySet().models(Note).load_all().auto_query(request.GET.get('q', ''))
        query = request.GET.get('q', '')
        searchresults = self._meta.queryset.filter(draft=0,deleted=0).filter(Q(title__icontains=query) | Q(description__icontains=query))
        paginator = Paginator(searchresults, 20)

        try:
            page = paginator.page(int(request.GET.get('page', 1)))
        except InvalidPage:
            raise Http404("Sorry, no results on that page.")

        objects = []

        for result in page.object_list:
            bundle = self.build_bundle(obj=result, request=request)
            bundle = self.full_dehydrate(bundle)
            objects.append(bundle)

        object_list = {
            'quizzes': objects,
        }

        self.log_throttled_access(request)
        return self.create_response(request, object_list)
    
        
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
        fields = ['title','type','id']
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
        include_resource_uri = True
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
   
    # add the quiz_id into the bundle
    def dehydrate(self, bundle, request=None):
        bundle.data['quiz_id'] = QuizResource().get_via_uri(bundle.data['quiz']).id
        return bundle
    
    # use this for filtering on the digest prop of a quiz to determine if it already exists
    # to avoid recreating the same quiz over and over
    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<digest>[\w\d_.-]+)/$" % self._meta.resource_name, self.wrap_view('digest_detail'), name="api_digest_detail"),
        ]
        
    def digest_detail(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)
        
        digest = kwargs.pop('digest', None)
        quizprop = self._meta.queryset.filter(name = 'digest').filter(value=digest)
        paginator = Paginator(quizprop, 20)

        try:
            page = paginator.page(int(request.GET.get('page', 1)))
        except InvalidPage:
            raise Http404("Sorry, no results on that page.")
        
        objects = []

        for result in page.object_list:
            bundle = self.build_bundle(obj=result, request=request)
            bundle = self.full_dehydrate(bundle)
            objects.append(bundle)

        object_list = {
            'quizzes': objects,
        }

        self.log_throttled_access(request)
        return self.create_response(request, object_list)

        
class RegisterResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'register'
        allowed_methods = ['post']
        fields = ['username', 'first_name','last_name','email']
        authorization = Authorization() 
        always_return_data = True 
        include_resource_uri = False
         
    def obj_create(self, bundle, request=None, **kwargs):
        data = { 'username': bundle.data['username'],
                'password': bundle.data['password'],
                'password_again': bundle.data['passwordagain'],
                'email': bundle.data['email'],
                'first_name': bundle.data['firstname'],
                'last_name': bundle.data['lastname'],}
        rf = RegisterForm(data)
        if not rf.is_valid():
            str = ""
            for key, value in rf.errors.items():
                for error in value:
                    str += error + "\n"
            raise BadRequest(str)
        else:
            username = bundle.data['username']
            password = bundle.data['password']
            email = bundle.data['email']
            first_name = bundle.data['firstname']
            last_name = bundle.data['lastname']
        try:
            bundle.obj = User.objects.create_user(username, email, password)
            bundle.obj.first_name = first_name
            bundle.obj.last_name = last_name
            bundle.obj.save()
            u = authenticate(username=username, password=password)
            if u is not None:
                if u.is_active:
                    login(bundle.request, u)
            key = ApiKey.objects.get(user = u)
            bundle.data['api_key'] = key.key
        except IntegrityError:
            # TODO translation
            raise BadRequest(_(u'Username "%s" already in use, please select another' % username))
        del bundle.data['passwordagain']
        del bundle.data['password']
        del bundle.data['firstname']
        del bundle.data['lastname']
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
        bundle.obj.ip = bundle.request.META.get('REMOTE_ADDR','0.0.0.0')
        bundle.obj.agent = bundle.request.META.get('HTTP_USER_AGENT','unknown')
        
        # get the question resource uri from the question id
        for response in bundle.data['responses']:
            # TODO should check that the question is actually in this quiz first
            # TODO what happens when the question has been deleted
            response['question'] = Question.objects.get(pk = response['question_id'])
        return bundle 
    