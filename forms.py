#mquiz/forms.py
from django import forms
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

class QuizForm(forms.Form):
    title = forms.CharField(max_length=200,
        error_messages={'invalid': _(u'Please enter a title.')},
        required=True)

