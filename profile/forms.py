from django import forms
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=30)
    email = forms.CharField(validators=[validate_email],
        error_messages={'invalid': _(u'Please enter a valid e-mail address.')},
        required=True)
    password = forms.CharField(widget=forms.PasswordInput,
        min_length=6,       
        required=True)
    password_again = forms.CharField(widget=forms.PasswordInput,
        min_length=6,
        required=True)
    first_name = forms.CharField(max_length=100,
        min_length=2,
        required=True)
    last_name = forms.CharField(max_length=100,
        min_length=2,
        required=True)

    def clean(self):
        cleaned_data = self.cleaned_data
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        password_again = cleaned_data.get("password_again")

        # check the email address not already used
        num_rows = User.objects.filter(email__exact=email).count()
        if num_rows != 0:
            raise forms.ValidationError("Email has already been registered")

        # check the password are the same
        if password and password_again:
            if password != password_again:
                raise forms.ValidationError("Passwords do not match.")

        # Always return the full collection of cleaned data.
        return cleaned_data

class ResetForm(forms.Form):
    email = forms.CharField(validators=[validate_email],
        error_messages={'invalid': _(u'Please enter a valid e-mail address.')},
        required=True)

