#mquiz/admin.py
from mquiz.models import Quiz,Question,Response
from django.contrib import admin

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Response)
