# mquiz_mobile/urls.py
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',

    url(r'^$',  'mquiz.mobile.views.index_view',name="mquiz_mobile"),    
    
)
