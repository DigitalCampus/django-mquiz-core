# mquiz/urls.py
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

from tastypie.api import Api
from mquiz.api.resources import QuizResource, UserResource, QuestionResource, RegisterResource
from mquiz.api.resources import QuizQuestionResource, ResponseResource, QuizPropsResource, QuestionPropsResource, ResponsePropsResource

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(QuizResource())
v1_api.register(QuizPropsResource())
v1_api.register(QuestionResource())
v1_api.register(QuestionPropsResource())
v1_api.register(QuizQuestionResource())
v1_api.register(ResponseResource())
v1_api.register(ResponsePropsResource())
v1_api.register(RegisterResource())

urlpatterns = patterns('',

    url(r'^$', 'mquiz.views.home_view', name="mquiz_home"),
    url(r'^about/about/$', direct_to_template, {"template": "mquiz/about.html",}, name="mquiz_about"),
    url(r'^about/terms/$', direct_to_template, {"template": "mquiz/terms.html",}, name="mquiz_terms"),
    url(r'^about/contact/$', direct_to_template, {"template": "mquiz/contact.html",}, name="mquiz_contact"),
    url(r'^create/$', 'mquiz.views.create', name="mquiz_create"),
    url(r'^m/', include('mquiz.mobile.urls')),
    (r'^api/', include(v1_api.urls)),

    

)
