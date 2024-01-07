import csv
import datetime
import json
from decimal import Decimal
from typing import Any

import requests
from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.list import ListView

from client.models import Account, Card, Client

from .forms import TransactionForm
from .models import Comission, Transaction
from .utils import calc_comission


@csrf_exempt
def transfer(request):
    data = json.loads(request.body)
    if {'business', 'ccc', 'pin', 'amount'} == set(data.keys()):
        if data['ccc'][:2] != 'C6':
            HttpResponseBadRequest('Unrecognized card')
        card_id = int(data['ccc'][3:])
        if card := Card.objects.get(id=card_id, pin=data['pin'], status=Card.States.ACTIVE):
            account = card.account
            amount = Decimal(data['amount'])
            comission_amount = calc_comission(
                amount, Comission.Type.PAYMENT, settings.COMISSION_TABLE
            )
            if amount + comission_amount <= account.balance:
                account.balance -= amount + comission_amount
                new_transaction = Transaction(
                    agent=data['business'],
                    amount=data['amount'],
                    concept='payment',
                    account=account,
                    kind=Transaction.Type.PAYMENT,
                )
                account.save()
                new_transaction.save()
                new_comission = Comission(
                    kind=Comission.Type.PAYMENT, transfer=new_transaction, amount=comission_amount
                )
                new_comission.save()
            return HttpResponse()
        else:
            return HttpResponseBadRequest('Unable to operate with the given card.')
    else:
        return HttpResponseBadRequest('Data not consistent with request.')


@csrf_exempt
def transfer_inc(request):
    data = json.loads(request.body)
    if {'sender', 'cac', 'concept', 'amount'} <= set(data.keys()):
        account_id = int(data['cac'][3:])
        if account := Account.objects.get(id=account_id, status=Account.States.ACTIVE):
            amount = Decimal(data['amount'])
            comission_amount = calc_comission(
                amount, Comission.Type.INCOMING, settings.COMISSION_TABLE
            )
            account.balance += amount - comission_amount
            new_transaction = Transaction(
                agent=data['sender'],
                amount=amount,
                concept=data['concept'],
                account=account,
                kind=Transaction.Type.INCOMING,
            )
            account.save()
            new_transaction.save()
            new_comission = Comission(
                kind=Comission.Type.INCOMING, transfer=new_transaction, amount=comission_amount
            )
            new_comission.save()
            return HttpResponse()
        else:
            return HttpResponseBadRequest('Unable to operate with the given account.')
    else:
        return HttpResponseBadRequest('Data not consistent with request.')


@csrf_exempt
@login_required
def transfer_out(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            agent_type, bank_id = cd['account'][:2]

            if agent_type == 'A' and int(bank_id) < len(settings.BANK_DATA):
                # bank_url = settings.BANK_DATA[int(bank_id) - 1]['url'] +':8000/transfer/incoming/'
                bank_url = 'http://127.0.0.1:8000/transfer/incoming/'
            else:
                return HttpResponseBadRequest('Unregistered entity.')
            account_id = cd['agent']
            account = Account.objects.get(id=account_id)
            amount = cd['amount']
            comission_amount = calc_comission(
                amount, Comission.Type.OUTGOING, settings.COMISSION_TABLE
            )
            if amount + comission_amount > account.balance:
                return HttpResponseBadRequest('Amount exceeds the account available money.')
            data = {
                'sender': account.alias,
                'cac': cd['account'],
                'concept': cd['concept'],
                'amount': str(amount),
            }
            response = requests.post(bank_url, json=data)
            if response.status_code == 200:
                account.balance -= amount + comission_amount
                new_transaction = Transaction(
                    agent=data['sender'],
                    amount=amount,
                    concept=data['concept'],
                    account=account,
                    kind=Comission.Type.OUTGOING,
                )
                new_comission = Comission(
                    kind=Comission.Type.OUTGOING, transfer=new_transaction, amount=comission_amount
                )
                account.save()
                new_transaction.save()
                new_comission.save()
                return render(request, 'transactions/transaction/done.html', {'form': form})
        messages.error(request, 'Unable to reach the recipient.')
        return render(request, 'transactions/transaction/create.html', {'form': form})
    else:
        user = Client.objects.get(user=request.user)
        if accounts := user.accounts.filter(status=Account.States.ACTIVE):
            form = TransactionForm()
            form.fields['agent'] = forms.ModelChoiceField(queryset=accounts)
        else:
            messages.error(
                request, 'You must have an active account in order to make a transaction.'
            )
            return HttpResponseRedirect('/client/')
    return render(request, 'transactions/transaction/create.html', {'form': form})


class TransactionListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        client = get_object_or_404(Client, user=self.request.user)
        if 'account_id' in self.request.GET.keys():
            account = get_object_or_404(
                Account, id=self.request.GET.get('account_id'), user=client.id
            )
            queryset = account.transactions.all()
        else:
            accounts = client.accounts.all()
            queryset = Transaction.objects.filter(account__in=accounts)
        return queryset

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['client'] = get_object_or_404(Client, user=self.request.user)
        return context

    paginate_by = 2
    context_object_name = 'transactions'
    template_name = 'transactions/movements.html'


@login_required
def transfer_detail(request, id):
    transaction = get_object_or_404(Transaction, id=id)
    return render(request, 'transactions/transaction/detail.html', {'transaction': transaction})


@login_required
def export_to_csv(request):
    client = get_object_or_404(Client, user=request.user)
    if 'account_id' in request.GET.keys():
        account = get_object_or_404(Account, id=request.GET.get('account_id'), user=client.id)
        queryset = account.transactions.all()
    else:
        accounts = client.accounts.all()
        queryset = Transaction.objects.filter(account__in=accounts)

    content_disposition = 'attachment; filename=movements.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)
    fields = [
        field
        for field in queryset[0]._meta.fields
        if not field.many_to_many and not field.one_to_many
    ]
    # Header
    writer.writerow([field.verbose_name for field in fields])
    # Datos
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response
