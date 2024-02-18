from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _

from transactions.models import Comission

from .forms import (
    AccountModificationForm,
    AccountRegistrationForm,
    CardCreationForm,
    CardModificationForm,
    ClientEditForm,
    ClientRegistrationForm,
    LoginForm,
    UserEditForm,
)
from .models import Account, Card, Client
from .utils import random_alphanum


def register(request):
    if request.method == 'POST':
        user_form = ClientRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Client.objects.create(user=new_user)
            return render(request, 'registration/register_done.html', {'new_user': new_user})
        else:
            return render(request, 'client/register.html', {'user_form': user_form})
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
                # todo
                return HttpResponse('Alias already in use.')
    else:
        form = AccountRegistrationForm()
        form.fields['user'] = Client.objects.get(user=request.user)
    return render(request, 'client/account/create_account.html', {'form': form})


@login_required
def modify_account(request, account_slug):
    form = AccountModificationForm(request.POST)
    if request.method == 'POST':
        user = Client.objects.get(user=request.user)
        accounts = user.accounts.all()
        account = Account.objects.get(user=user, slug=account_slug)
        if not account_slug:
            account = Account.objects.get(user=user, slug=accounts[0].slug)
        if form.is_valid():
            account.alias = form.cleaned_data['alias']
            account.status = form.cleaned_data['status']
            account.save()
            return redirect('dashboard')
    else:
        form = AccountModificationForm(instance=get_object_or_404(Account, slug=account_slug))
    return render(request, 'client/account/modify_account.html', {'form': form})


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
                # todo
                return HttpResponse('Unable to create card')
    else:
        form = CardCreationForm()
        form.fields['account'].queryset = Account.objects.filter(user=user)
    return render(request, 'client/card/create_card.html', {'form': form})


@login_required
def modify_card(request, card_id):
    if request.method == 'POST':
        form = CardModificationForm(request.POST)
        user = Client.objects.get(user=request.user)
        card = Card.objects.get(user=user, id=card_id)
        if form.is_valid():
            card.alias = form.cleaned_data['alias']
            card.status = form.cleaned_data['status']
            card.save()
            return redirect('dashboard')
    else:
        form = CardModificationForm(instance=get_object_or_404(Card, id=card_id))
    return render(request, 'client/card/modify_card.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                client = get_object_or_404(Client, user=user)
                if client.status == Client.States.ACTIVE:
                    login(request, user)
                    return redirect('dashboard')
                else:
                    error = _('Client not active')
            else:
                error = _('Invalid Login')
            messages.error(request, error)
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ClientEditForm(instance=request.user, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return render(
                request,
                'client/edit_done.html',
                {'user_form': user_form, 'profile_form': profile_form},
            )
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ClientEditForm(instance=request.user)
    return render(
        request, 'client/edit.html', {'user_form': user_form, 'profile_form': profile_form}
    )


@login_required
def dashboard(request, account_slug=None):
    client = get_object_or_404(Client, user=request.user)
    if accounts := client.accounts.all():
        if account_slug:
            acc_detail = get_object_or_404(accounts, slug=account_slug)
        else:
            acc_detail = accounts[0]
        datetime_reference = datetime.now() - timedelta(days=30)
        period_movements = acc_detail.transactions.filter(timestamp__gte=datetime_reference)
        period_comissions = Comission.objects.filter(transfer__in=period_movements)
        income = sum(movement.amount for movement in period_movements.filter(kind='INC'))
        expenses = sum(movement.amount for movement in period_movements.filter(kind='OUT')) + sum(
            comission.amount for comission in period_comissions
        )
    else:
        acc_detail = income = expenses = None
    return render(
        request,
        'client/dashboard.html',
        {
            'accounts': accounts,
            'acc_detail': acc_detail,
            'income': income,
            'expenses': expenses,
        },
    )
