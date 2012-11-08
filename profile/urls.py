# mquiz/profile/urls.py
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',

    url(r'^register/$', 'mquiz.profile.views.register', name="profile_register"),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'mquiz/login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'mquiz/logout.html'}),
    url(r'^thanks/$', direct_to_template, {"template": "mquiz/thanks.html",}, name="profile_register_thanks"),
    url(r'^setlang/$', 'django.views.i18n.set_language', name="profile_set_language"),
    url(r'^reset/$', 'mquiz.profile.views.reset', name="profile_reset"),
    
)