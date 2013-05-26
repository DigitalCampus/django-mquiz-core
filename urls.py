# mquiz/urls.py
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from mquiz.feeds import LatestQuizzesFeed, RecentActivityFeed

urlpatterns = patterns('',
    url(r'^scoreboard/$', 'mquiz.views.scoreboard_view', name="mquiz_scoreboard"),
    url(r'^quiz/(?P<quiz_id>\d+)/edit/$', 'mquiz.quiz.quiz.edit_quiz', name="mquiz_edit"),
    url(r'^quiz/(?P<quiz_id>\d+)/saved/$',  'mquiz.quiz.quiz.saved_quiz', name="mquiz_edit_saved"),
    url(r'^quiz/(?P<quiz_id>\d+)/delete/$', 'mquiz.quiz.quiz.delete_quiz', name="mquiz_delete"),
    url(r'^quiz/(?P<quiz_id>\d+)/deleted/$', 'mquiz.quiz.quiz.deleted_quiz', name="mquiz_deleted"),
    url(r'^quiz/(?P<quiz_id>\d+)/results/date/$', 'mquiz.quiz.reporting.quiz_results_date', name="mquiz_results_date"),
    url(r'^quiz/(?P<quiz_id>\d+)/results/score/$', 'mquiz.quiz.reporting.quiz_results_score', name="mquiz_results_score"),
    url(r'^quiz/(?P<quiz_id>\d+)/results/questions/$', 'mquiz.quiz.reporting.quiz_results_questions', name="mquiz_results_questions"),
    url(r'^quiz/(?P<quiz_id>\d+)/results/attempts/$', 'mquiz.quiz.reporting.quiz_results_attempts', name="mquiz_results_attempts"),
    url(r'^quiz/create/$', 'mquiz.quiz.quiz.create_quiz', name="mquiz_create"),
    url(r'^m/', include('mquiz.mobile.urls')),
    url(r'^browse/$', 'mquiz.views.browse', name="mquiz_browse"),
    url(r'^browse/(?P<letter>\w+)$', 'mquiz.views.browse', name="mquiz_browse_alpha"),
    url(r'^results/my/$', 'mquiz.quiz.reporting.my_results', name="mquiz_my_results"),
    url(r'^manage/$', 'mquiz.views.manage_view', name="mquiz_manage"), 
    url(r'^rss/latest/$', LatestQuizzesFeed(), name="mquiz_rss_latest"),
    url(r'^rss/attempts/$', RecentActivityFeed(), name="mquiz_rss_attempts"),
    # TODO customise name (currently api_v1_top_level)
    url(r'^api/', include('mquiz.api.urls')),
)
