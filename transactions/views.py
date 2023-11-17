import json
from decimal import Decimal
from typing import Any

import requests
from django import forms
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.list import ListView

from client.models import Account, Card, Client

from .forms import TransactionForm
from .models import Transaction


@csrf_exempt
def transfer(request):
    # request.body contiene el json con los datos
    data = json.loads(request.body)
    # En data tendremos un diccionario con los datos enviados

    if {'business', 'ccc', 'pin', 'amount'} == set(data.keys()):
        # se podría comprobar que es el banco correcto, evitando así atacar la DB
        bank_id = data['ccc'][:2]
        card_id = int(data['ccc'][3:])
        amount = Decimal(data['amount'])
        # comprobar banco ...
        # comprobar tarjeta y pin, falta hashear todo
        try:
            card = Card.objects.get(id=card_id, pin=data['pin'])
            target_account = card.account
        except Exception:
            return HttpResponseForbidden()
        # comprobar que haya dinero para realizar cobro
        if amount <= target_account.balance:
            target_account.balance = target_account.balance - amount
            new_transaction = Transaction(
                agent=data['business'],
                amount=data['amount'],
                concept='payment',
                account=target_account,
                kind='PAY',
            )
            target_account.save()
            new_transaction.save()
        return HttpResponse()
    else:
        return HttpResponseBadRequest()


@csrf_exempt
def transfer_inc(request):
    data = json.loads(request.body)
    # En data tendremos un diccionario con los datos enviados
    if ['sender', 'cac', 'concept', 'amount'] == [key for key in data.keys()]:
        bank_id = data['cac'][:2]
        account_id = int(data['cac'][3:])
        amount = Decimal(data['amount'])
        try:
            account = Account.objects.get(id=account_id)
        except Exception:
            return HttpResponseBadRequest('No ha sido posible realizar la operación')
        account.balance = account.balance + amount
        new_transaction = Transaction(
            agent=data['sender'],
            amount=amount,
            concept=data['concept'],
            account=account,
            kind='INC',
        )
        account.save()
        new_transaction.save()
        return HttpResponse(account)
    else:
        return HttpResponseBadRequest('Los datos de la operación son incorrectos')


@csrf_exempt
@login_required
def transfer_out(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            agent_type, bank_id = cd['account'][:2]

            if agent_type == 'A' and int(bank_id) < len(settings.BANK_DATA):
                bank_url = settings.BANK_DATA[int(bank_id) - 1]['url'] + ':8000/transfer/incoming/'
            else:
                raise HttpResponseBadRequest('No')
            account_id = cd['agent']
            account = Account.objects.get(id=account_id)
            amount = cd['amount']
            for k, v in settings.COMISSION_TABLE.items():
                if amount < k:
                    comission_amount = amount * Decimal(v['OUT']) / 100
                    break
            if amount + comission_amount > account.balance:
                return HttpResponseBadRequest('No es posible realizar la operación')
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
                    kind='OUT',
                )                
                account.save()
                new_transaction.save()
                return render(request, 'transactions/transaction/done.html', {'form': form})
        return render(request, 'transactions/transaction/create.html', {'form': form})
    else:
        form = TransactionForm()
        user = Client.objects.get(user=request.user)
        form.fields['agent'] = forms.ModelChoiceField(queryset=user.accounts.all())
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
