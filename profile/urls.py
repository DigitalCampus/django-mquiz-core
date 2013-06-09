# mquiz/profile/urls.py
from django.conf.urls.defaults import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',

    url(r'^register/$', 'mquiz.profile.views.register', name="profile_register"),
    url(r'^register/thanks/$', TemplateView.as_view(template_name="mquiz/thanks.html"), name="profile_register_thanks"),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'mquiz/login.html',}),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'mquiz/logout.html',}),
    url(r'^setlang/$', 'django.views.i18n.set_language', name="profile_set_language"),
    url(r'^reset/$', 'mquiz.profile.views.reset', name="profile_reset"),
    url(r'^reset/sent/$', TemplateView.as_view(template_name="mquiz/profile/reset-sent.html"), name="profile_reset_sent"),
    url(r'^edit/$', 'mquiz.profile.views.edit', name="profile_edit"),
    url(r'^points/$', 'mquiz.profile.views.points', name="profile_points"),
    url(r'^badges/$', 'mquiz.profile.views.badges', name="profile_badges"),
)
