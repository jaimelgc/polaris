from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from .forms import ClientRegistrationForm, LoginForm
from .models import Client


def register(request):
    if request.method == 'POST':
        user_form = ClientRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            # Create profile of the user (create saves to db)
            Client.objects.create(user=new_user)
            # show the user an alternative url
            # pass the client instead of the user, evaluate implications
            return render(request, 'client/register_done.html', {'new_user': new_user})
    else:
        user_form = ClientRegistrationForm()
    return render(request, 'client/register.html', {'user_form': user_form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse('Authenticated successfully')
            else:
                return HttpResponse('Disabled account')
        else:
            return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'client/login.html', {'form': form})


@login_required
def dashboard(request):
    return render(request, 'client/dashboard.html/')
