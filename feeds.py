# mquiz/feeds.py
from django.contrib.syndication.views import Feed
from mquiz.models import Quiz
from django.conf import settings
from django.core.urlresolvers import reverse

class LatestQuizzesFeed(Feed):
    title = "mQuiz latest quizzes"
    link = "/"
    description = "Latest quizzes created on mQuiz"

    def items(self):
        return Quiz.objects.order_by('-created_date')[:10]

    def item_title(self, item):
        return item.title

    def item_pubdate(self, item):
        return item.created_date
    
    def item_description(self, item):
        return item.description
    
    def item_link(self,item):
        return settings.SITE_URL + reverse('mquiz_mobile_quiz', args=[item.pk])