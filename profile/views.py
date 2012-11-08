from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import (authenticate, login, views)
from django.contrib.auth.models import User
from django.core.mail import send_mail

from forms import RegisterForm, ResetForm

def register(request):
    if request.method == 'POST': # if form submitted...
        form = RegisterForm(request.POST)
        if form.is_valid(): # All validation rules pass
            # Create new user
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            u = authenticate(username=username, password=password)
            if u is not None:
                if u.is_active:
                    login(request, u)
                    return render(request, 'mquiz/thanks.html') # Redirect after POST
            return render(request, 'mquiz/thanks.html') # Redirect after POST
    else:
        form = RegisterForm() # An unbound form

    return render(request, 'mquiz/register.html', {'form': form,})

def reset(request):
    if request.method == 'POST': # if form submitted...
        form = ResetForm(request.POST)
        send_mail('Subject here', 'Here is the message.', 'alex@digital-campus.org',
    ['alex@alexlittle.net'], fail_silently=False)
    else:
        form = ResetForm() # An unbound form

    return render(request, 'mquiz/reset.html', {'form': form,})


