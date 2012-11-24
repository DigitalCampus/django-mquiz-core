# mquiz/forms.py
from django import forms
from django.forms import ModelForm
from django.forms.formsets import BaseFormSet
from django.forms.models import inlineformset_factory  
from mquiz.models import Quiz, Question, Response

ResponseFormset = inlineformset_factory(Question, Response, extra=4) 

class BaseQuestionFormSet(BaseFormSet):
    def add_fields(self, form, index):
        super(BaseQuestionFormSet, self).add_fields(form, index)
        # created the nested formset
        try:
            instance = self.get_queryset()[index]
            pk_value = instance.pk
        except IndexError:
            instance=None
            pk_value = hash(form.prefix)
 
        # store the formset in the .nested property
        form.nested = [
            ResponseFormset(data=self.data,
                            instance = instance,
                            prefix = 'RESPONSES_%s' % pk_value)]
        
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

