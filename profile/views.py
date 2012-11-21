from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import (authenticate, login, views)
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

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
        if form.is_valid():
            username = form.cleaned_data.get("username")
            user = User.objects.get(username__exact=username)
            newpass = User.objects.make_random_password(length=8)
            user.set_password(newpass)
            user.save()
            # TODO - better way to manage email message content
            # TODO use
            send_mail('mQuiz: Password reset', 'Here is your new password for mQuiz: '+newpass 
                      + '\n\nWhen you next log in you can update your password to something more memorable.' 
                      + '\n\nhttp://mquiz.org', 
                      settings.SERVER_EMAIL, [user.email], fail_silently=False)
            return render(request, 'mquiz/reset-sent.html')
    else:
        form = ResetForm() # An unbound form

    return render(request, 'mquiz/reset.html', {'form': form,})


