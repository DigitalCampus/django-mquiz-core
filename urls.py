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
    url(r'^about/$', 'mquiz.views.about_view', name="mquiz_about"),
    url(r'^terms/$', 'mquiz.views.terms_view', name="mquiz_terms"),
    url(r'^contact/$', 'mquiz.views.contact_view', name="mquiz_contact"),
    url(r'^quiz/(?P<quiz_id>\d+)/edit/$', 'mquiz.views.edit_quiz', name="mquiz_edit"),
    url(r'^quiz/(?P<quiz_id>\d+)/delete/$', 'mquiz.views.delete_quiz', name="mquiz_delete"),
    url(r'^quiz/(?P<quiz_id>\d+)/results/date/$', 'mquiz.views.quiz_results_date', name="mquiz_results_date"),
    url(r'^quiz/(?P<quiz_id>\d+)/results/score/$', 'mquiz.views.quiz_results_score', name="mquiz_results_score"),
    url(r'^quiz/(?P<quiz_id>\d+)/results/questions/$', 'mquiz.views.quiz_results_questions', name="mquiz_results_questions"),
    url(r'^quiz/(?P<quiz_id>\d+)/results/attempts/$', 'mquiz.views.quiz_results_attempts', name="mquiz_results_attempts"),
    url(r'^quiz/create/$', 'mquiz.views.create_quiz', name="mquiz_create"),
    url(r'^quiz/create/saved/$', direct_to_template, {"template": "mquiz/quiz/saved.html",}, name="mquiz_create_saved"),
    url(r'^m/', include('mquiz.mobile.urls')),
    url(r'^profile/', include('mquiz.profile.urls')),
    url(r'^browse/$', 'mquiz.views.browse', name="mquiz_browse"),
    url(r'^browse/(?P<letter>\w+)$', 'mquiz.views.browse', name="mquiz_browse_alpha"),
    url(r'^results/my/$', 'mquiz.views.my_results', name="mquiz_my_results"),
    url(r'^manage/$', 'mquiz.views.manage_view', name="mquiz_manage"), 
    
    # TODO customise name (currently api_v1_top_level)
    url(r'^api/', include(v1_api.urls)),

)
