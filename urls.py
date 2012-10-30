#mquiz/urls.py
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from tastypie.api import Api

from mquiz.api import QuizResource, UserResource

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(QuizResource())

urlpatterns = patterns('',

    url(r'^$', 'mquiz.views.home_view', name="mquiz_home"),
    url(r'^about/about/$', direct_to_template, {"template": "mquiz/about.html",}, name="mquiz_about"),
    url(r'^about/terms/$', direct_to_template, {"template": "mquiz/terms.html",}, name="mquiz_terms"),
    url(r'^about/contact/$', direct_to_template, {"template": "mquiz/contact.html",}, name="mquiz_contact"),
    url(r'^create/$', 'mquiz.views.create', name="mquiz_create"),
    
    (r'^api/', include(v1_api.urls)),
)
