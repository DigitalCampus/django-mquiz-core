# mquiz_mobile/urls.py
from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',

    url(r'^$',  'mquiz.mobile.views.index_view',name="mquiz_mobile"), 
    url(r'^#(?P<quiz_id>\d+)$',  'mquiz.mobile.views.index_view',name="mquiz_mobile_quiz")       
)
