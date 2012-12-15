# mquiz/feeds.py
from django.contrib.syndication.views import Feed
from mquiz.models import Quiz, QuizAttempt
from django.conf import settings
from django.core.urlresolvers import reverse

class LatestQuizzesFeed(Feed):
    title = "mQuiz latest quizzes"
    link = "/"
    description = "Latest quizzes created on mQuiz"

    def items(self):
        return Quiz.objects.filter(deleted=0,draft=0).order_by('-created_date')[:10]

    def item_title(self, item):
        return item.title

    def item_pubdate(self, item):
        return item.created_date
    
    def item_description(self, item):
        return item.description
    
    def item_link(self,item):
        return settings.SITE_URL + reverse('mquiz_mobile_quiz', args=[item.pk])
    
    
class RecentActivityFeed(Feed):
    title = "mQuiz latest activity"
    link = "/"
    description = "Latest activity"

    def items(self):
        return QuizAttempt.objects.all().order_by('-submitted_date')[:10]

    def item_title(self, item):
        return item.quiz.title + " completed"

    def item_pubdate(self, item):
        return item.submitted_date
    
    def item_description(self, item):
        return "by " + item.user.username
    
    def item_link(self,item):
        return settings.SITE_URL + reverse('mquiz_results_date', args=[item.quiz.id])