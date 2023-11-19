from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .forms import (
    AccountRegistrationForm,
    CardCreationForm,
    ClientRegistrationForm,
    LoginForm,
)
from .models import Account, Client
from .utils import random_alphanum


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


@login_required
def create_account(request):
    if request.method == 'POST':
        form = AccountRegistrationForm(request.POST)
        if form.is_valid():
            user = Client.objects.get(user=request.user)
            if not user.accounts.filter(alias=form.cleaned_data['alias']).exists():
                new_account = form.save(commit=False)
                new_account.user = Client.objects.get(user=request.user)
                new_account.save()
                return render(request, 'client/account/account_done.html', {'form': form})
            else:
                return HttpResponse('Alias already in use.')
    else:
        form = AccountRegistrationForm()
        form.fields['user'] = Client.objects.get(user=request.user)
    return render(request, 'client/account/create_account.html', {'form': form})


@login_required
def create_card(request):
    user = Client.objects.get(user=request.user)
    if request.method == 'POST':
        form = CardCreationForm(request.POST)
        if form.is_valid():
            if not user.cards.filter(alias=form.cleaned_data['alias']).exists():
                new_card = form.save(commit=False)
                new_card.pin = random_alphanum(3)
                new_card.user = user
                new_card.save()
                return render(request, 'client/card/card_done.html', {'form': form})
            else:
                return HttpResponse('Unable to create card')
        else:
            print(form.errors.as_data)
    else:
        form = CardCreationForm()
        form.fields['account'].queryset = Account.objects.filter(user=user)
    return render(request, 'client/card/create_card.html', {'form': form})


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
def dashboard(request, account_slug=None):
    client = get_object_or_404(Client, user=request.user)
    if accounts := client.accounts.all():
        if account_slug:
            acc_detail = get_object_or_404(accounts, slug=account_slug)
        else:
            acc_detail = get_object_or_404(accounts, slug=accounts[0].slug)
    else:
        acc_detail = None
    return render(
        request,
        'client/dashboard.html',
        {
            'accounts': accounts,
            'acc_detail': acc_detail,
        },
    )
