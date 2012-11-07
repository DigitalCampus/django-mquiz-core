# mquiz/admin.py
from mquiz.models import Quiz,Question,Response,ResponseProps,QuestionProps,QuizProps,QuizQuestion
from django.contrib import admin

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Response)
admin.site.register(ResponseProps)
admin.site.register(QuestionProps)
admin.site.register(QuizProps)
admin.site.register(QuizQuestion)
