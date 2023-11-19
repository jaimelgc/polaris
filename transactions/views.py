import json
from decimal import Decimal
from typing import Any

import requests
from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponseRedirect,
)
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.list import ListView

from client.models import Account, Card, Client
from client.utils import calc_comission

from .forms import TransactionForm
from .models import Comission, Transaction


@csrf_exempt
def transfer(request):
    # request.body contiene el json con los datos
    data = json.loads(request.body)
    # En data tendremos un diccionario con los datos enviados

    if {'business', 'ccc', 'pin', 'amount'} == set(data.keys()):
        # se podría comprobar que es el banco correcto, evitando así atacar la DB
        if data['ccc'][:2] != 'C6':
            HttpResponseBadRequest('Unrecognized card')
        card_id = int(data['ccc'][3:])
        # comprobar banco ...
        # comprobar tarjeta y pin, falta hashear todo
        try:
            card = Card.objects.get(id=card_id, pin=data['pin'])
            account = card.account
        except Exception:
            return HttpResponseForbidden()
        amount = Decimal(data['amount'])
        comission_amount = calc_comission(amount, Comission.Type.PAYMENT, settings.COMISSION_TABLE)
        # comprobar que haya dinero para realizar cobro
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
        return HttpResponseBadRequest()


@csrf_exempt
def transfer_inc(request):
    data = json.loads(request.body)
    # En data tendremos un diccionario con los datos enviados
    if {'sender', 'cac', 'concept', 'amount'} <= set(data.keys()):
        account_id = int(data['cac'][3:])
        try:
            account = Account.objects.get(id=account_id)
        except Exception:
            return HttpResponseBadRequest('No ha sido posible realizar la operación')
        amount = Decimal(data['amount'])
        comission_amount = calc_comission(amount, Comission.Type.INCOMING, settings.COMISSION_TABLE)
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
                # bank_url = settings.BANK_DATA[int(bank_id) - 1]['url'] + ':8000/transfer/incoming/'
                bank_url = 'http://127.0.0.1:8000/transfer/incoming/'
            else:
                raise HttpResponseBadRequest('No puedes pasar')
            account_id = cd['agent']
            account = Account.objects.get(id=account_id)
            amount = cd['amount']
            comission_amount = calc_comission(
                amount, Comission.Type.OUTGOING, settings.COMISSION_TABLE
            )
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
                    kind=Comission.Type.OUTGOING,
                )
                new_comission = Comission(
                    kind=Comission.Type.OUTGOING, transfer=new_transaction, amount=comission_amount
                )
                account.save()
                new_transaction.save()
                new_comission.save()
                return render(request, 'transactions/transaction/done.html', {'form': form})
        return render(request, 'transactions/transaction/create.html', {'form': form})
    else:
        user = Client.objects.get(user=request.user)
        if accounts := user.accounts.all():
            form = TransactionForm()
            form.fields['agent'] = forms.ModelChoiceField(queryset=accounts)
        else:
            messages.error(request, 'You must have an account in order to make a transaction.')
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
