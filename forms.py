#mquiz/forms.py
from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext as _
from mquiz.models import Quiz, Question, Response

class QuizForm(ModelForm):
    class Meta:
        model = Quiz
        fields = ('title', 'description')
        widgets = {
            'title': forms.TextInput(),     
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 3}),
        }
    
    
class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ('title', 'type')
        widgets = {     
            'title': forms.Textarea(attrs={'cols': 80, 'rows': 3}),
        }
    
    
class ResponseForm(ModelForm):
    class Meta:
        model = Response
        fields = ('title', 'score')
        widgets = {     
            'title': forms.TextInput(),
            'score': forms.DecimalField,
        }

