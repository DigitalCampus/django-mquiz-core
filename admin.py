# mquiz/admin.py
from mquiz.models import Quiz,Question,Response,ResponseProps,QuestionProps,QuizProps,QuizQuestion, QuizAttempt, QuizAttemptResponse
from django.contrib import admin

class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'attempt_date', 'score', 'ip', 'instance_id')
    
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Response)
admin.site.register(ResponseProps)
admin.site.register(QuestionProps)
admin.site.register(QuizProps)
admin.site.register(QuizQuestion)
admin.site.register(QuizAttempt,QuizAttemptAdmin)
admin.site.register(QuizAttemptResponse)
