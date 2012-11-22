#mquiz/forms.py
from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext as _
from mquiz.models import Quiz

class QuizForm(ModelForm):
    class Meta:
        model = Quiz
        fields = ('title', 'description')
        widgets = {
            'title': forms.TextInput(),     
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 3}),
        }
    
    
class QuestionForm(forms.Form):
    title = forms.CharField(error_messages={'invalid': _(u'Please enter a title.')},
                            required=True,
                            widget=forms.Textarea(attrs={'cols': 80, 'rows': 3}),)
    
    
class ResponseForm(forms.Form):
    title = forms.CharField(max_length=200,
                            error_messages={'invalid': _(u'Please enter a title.')},
                            required=True,)

