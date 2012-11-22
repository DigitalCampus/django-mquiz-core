# mquiz/urls.py
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

from tastypie.api import Api
from mquiz.api.resources import QuizResource, UserResource, QuestionResource, RegisterResource, QuizAttemptResource
from mquiz.api.resources import QuizQuestionResource, ResponseResource, QuizPropsResource

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(QuizResource())
v1_api.register(QuizPropsResource())
v1_api.register(QuestionResource())
v1_api.register(QuizQuestionResource())
v1_api.register(ResponseResource())
v1_api.register(RegisterResource())
v1_api.register(QuizAttemptResource())

urlpatterns = patterns('',

    url(r'^$', 'mquiz.views.home_view', name="mquiz_home"),
    url(r'^about/$', direct_to_template, {"template": "mquiz/about.html",}, name="mquiz_about"),
    url(r'^terms/$', direct_to_template, {"template": "mquiz/terms.html",}, name="mquiz_terms"),
    url(r'^contact/$', direct_to_template, {"template": "mquiz/contact.html",}, name="mquiz_contact"),
    url(r'^create/$', 'mquiz.views.create_quiz', name="mquiz_create"),
    url(r'^create/saved/$', direct_to_template, {"template": "mquiz/quiz/saved.html",}, name="mquiz_create_saved"),
    url(r'^m/', include('mquiz.mobile.urls')),
    url(r'^profile/', include('mquiz.profile.urls')),
    # TODO customise name (currently api_v1_top_level)
    url(r'^api/', include(v1_api.urls), name="mquiz_api"),

    

)
