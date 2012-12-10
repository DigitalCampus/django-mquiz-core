# mquiz/forms.py
from django import forms
from django.forms import ModelForm
from mquiz.models import Quiz, Question, Response
from django.utils.translation import ugettext as _
import decimal
import re
from django.forms.formsets import BaseFormSet

class QuizForm(ModelForm):
    class Meta:
        model = Quiz
        fields = ('title', 'description')
        widgets = {
            'title': forms.TextInput(attrs={'size':'60'}),     
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 3}),
        }
        
class BaseQuestionFormSet(BaseFormSet):
    def clean(self):
        if self.total_form_count() == 0:
            raise forms.ValidationError(_(u"You must enter at least one question"))
        
class QuestionForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'size':'60'}))
    type = forms.ChoiceField(choices=Question.QUESTION_TYPES)
    # TODO this is really wrong - but couldn't get this working with inline formsets of ResponseForms
    response1 = forms.CharField(required=False)
    score1 = forms.DecimalField(required=False,initial=0)
    feedback1 = forms.CharField(required=False)
    response2 = forms.CharField(required=False)
    score2 = forms.DecimalField(required=False,initial=0)
    feedback2 = forms.CharField(required=False)
    response3 = forms.CharField(required=False)
    score3 = forms.DecimalField(required=False,initial=0)
    feedback3 = forms.CharField(required=False)
    response4 = forms.CharField(required=False)
    score4 = forms.DecimalField(required=False,initial=0)
    feedback4    = forms.CharField(required=False)
    
    def clean(self):
        cleaned_data = self.cleaned_data
        type = cleaned_data.get("type")
        # check question type for whether there should be answers or not
        needs_answers = True
        if type == 'essay' or type=='info':
            needs_answers = False
            
        if needs_answers:
            response1 = cleaned_data.get("response1").strip()
            if response1 == "":
                raise forms.ValidationError( _(u"You must enter at least one response"))
            
            # check at least one of the scores is none zero
            total_score = 0
            no_actual_responses = 0
            no_actual_scores = 0
            for i in range(1,4):
                response = cleaned_data.get("response"+str(i)).strip()
                score = cleaned_data.get("score"+str(i))
                if response != "":
                    if not isinstance(score, (int, float, decimal.Decimal)):
                        raise forms.ValidationError( _(u"All scores must be numerical values"))
                    total_score = total_score + score
                    no_actual_responses = no_actual_responses + 1
                    if score > 0:
                        no_actual_scores = no_actual_scores + 1
                    
                    # checks based on question type
                    # if numerical then must be numerical answer
                    if type == 'numerical':
                        try:
                            resp = float(response)
                        except:
                            resp = ""
                        if not isinstance(resp, float):
                            raise forms.ValidationError( _(u"For numerical question types the answer must be a number"))
                    # if matching then must be separated by a pipe char
                    if type == 'matching':
                        matches = re.split("\|",response)
                        if len(matches) != 2:
                            raise forms.ValidationError( _(u"For matching question types each response must have two parts separated by a '|' character, e.g. 'mouse|cheese'"))
                        
            # checks based on number of responses needed
            # multichoice > 1
            if type=='multichoice' and no_actual_responses < 2:
                raise forms.ValidationError( _(u"Multiple choice questions should have 2 or more possible responses"))
            # multiselect > 1 and TODO scores > 1
            if type=='multiselect' and no_actual_responses < 2:
                raise forms.ValidationError( _(u"Multiple select questions should have 2 or more possible responses"))
            # matching > 1
            if type=='matching' and no_actual_responses < 2:
                raise forms.ValidationError( _(u"Matching questions should have 2 or more possible responses"))
            
            if total_score == 0:
                raise forms.ValidationError( _(u"You must enter at least one non-zero score"))
             
        return cleaned_data
