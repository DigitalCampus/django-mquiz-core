# mquiz/forms.py
from django import forms
from django.forms import ModelForm
from mquiz.models import Quiz, Question, Response
from django.utils.translation import ugettext as _

class QuizForm(ModelForm):
    class Meta:
        model = Quiz
        fields = ('title', 'description')
        widgets = {
            'title': forms.TextInput(attrs={'size':'60'}),     
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 3}),
        }
    
class QuestionForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'size':'60'}))
    type = forms.ChoiceField(choices=Question.QUESTION_TYPES)
    # TODO this is really wrong - but couldn't get this working with inline formsets of ResponseForms
    response1 = forms.CharField()
    score1 = forms.DecimalField()
    response2 = forms.CharField()
    score2 = forms.DecimalField()
    response3 = forms.CharField()
    score3 = forms.DecimalField()
    response4 = forms.CharField()
    score4 = forms.DecimalField()
    
    
class ResponseForm(ModelForm):
    class Meta:
        model = Response
        fields = ('title', 'score')
        widgets = {     
            'title': forms.TextInput(),
            'score': forms.DecimalField,
        }

