import csv
import json
from decimal import Decimal
from typing import Any

import requests
import weasyprint
from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from client.models import Account, Card, Client

from .forms import TransactionForm
from .models import Comission, Transaction
from .utils import calc_comission


@csrf_exempt
def transfer(request):
    data = json.loads(request.body)
    if {'business', 'ccc', 'pin', 'amount'} == set(data.keys()):
        if data['ccc'][:2] != settings.BANK_CARD_CODE:
            error = _('Unrecognized card')
            return render(
                request,
                'transactions/transaction/error.html',
                {'error': error},
            )
        card_id = int(data['ccc'][3:])
        if card := get_object_or_404(Card, id=card_id, pin=data['pin'], status=Card.States.ACTIVE):
            account = card.account
            amount = Decimal(data['amount'])
            comission_amount = calc_comission(
                amount,
                Comission.Type.PAYMENT,
                settings.COMISSION_TABLE,
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
                    kind=Comission.Type.PAYMENT,
                    transfer=new_transaction,
                    amount=comission_amount,
                )
                new_comission.save()
            return HttpResponse()
        else:
            error = _('Unable to operate with the given card')
            return render(
                request,
                'transactions/transaction/error.html',
                {'error': error},
            )
    else:
        error = _('Data not consistent with request')
        return render(
            request,
            'transactions/transaction/error.html',
            {'error': error},
        )


@csrf_exempt
def transfer_inc(request):
    data = json.loads(request.body)
    if {'sender', 'cac', 'concept', 'amount'} <= set(data.keys()):
        account_id = int(data['cac'][3:])
        if account := get_object_or_404(Account, id=account_id, status=Account.States.ACTIVE):
            amount = Decimal(data['amount'])
            comission_amount = calc_comission(
                amount,
                Comission.Type.INCOMING,
                settings.COMISSION_TABLE,
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
                kind=Comission.Type.INCOMING,
                transfer=new_transaction,
                amount=comission_amount,
            )
            new_comission.save()

            return HttpResponse()
        else:
            error = _('Unable to operate with the given account')
            return render(
                request,
                'transactions/transaction/error.html',
                {'error': error},
            )
    else:
        error = _('Data not consistent with request')
        return render(
            request,
            'transactions/transaction/error.html',
            {'error': error},
        )


@csrf_exempt
@login_required
def transfer_out(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            agent_type, bank_id = cd['account'][:2]
            if agent_type == 'A' and int(bank_id) < len(settings.BANK_DATA):
                bank_url = settings.BANK_DATA[int(bank_id)]['url'] + '/transfer/incoming/'
            else:
                error = _('Unregistered entity')
                return render(
                    request,
                    'transactions/transaction/error.html',
                    {'error': error},
                )
            account_id = cd['agent']
            account = get_object_or_404(Account, id=account_id)
            amount = cd['amount']
            comission_amount = calc_comission(
                amount,
                Comission.Type.OUTGOING,
                settings.COMISSION_TABLE,
            )
            if amount + comission_amount > account.balance:
                error = _("Amount exceeds account\'s available money")
                return render(
                    request,
                    'transactions/transaction/error.html',
                    {'error': error},
                )
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
                    agent=account.alias,
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
                return render(
                    request,
                    'transactions/transaction/done.html',
                    {'form': form, 'transaction': new_transaction},
                )
        messages.error(request, _('Unable to reach the recipient.'))
        return render(request, 'transactions/transaction/create.html', {'form': form})
    else:
        user = Client.objects.get(user=request.user)
        if accounts := user.accounts.filter(status=Account.States.ACTIVE):
            form = TransactionForm()
            form.fields['agent'] = forms.ModelChoiceField(label=_('Agent'), queryset=accounts)
        else:
            messages.error(
                request, _('You must have an active account in order to make a transaction.')
            )
            return HttpResponseRedirect('/client/')
    return render(request, 'transactions/transaction/create.html', {'form': form})


def get_queryset(request):
    client = get_object_or_404(Client, user=request.user)
    if 'account_id' in request.GET.keys():
        account = get_object_or_404(Account, id=request.GET.get('account_id'), user=client.id)
        queryset = account.transactions.all()
    else:
        accounts = client.accounts.all()
        queryset = Transaction.objects.filter(account__in=accounts)
    return queryset


@login_required
def transfer_detail(request, id):
    transaction = get_object_or_404(Transaction, id=id)
    return render(request, 'transactions/transaction/detail.html', {'transaction': transaction})


@login_required
def transaction_pdf(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    html = render_to_string('transactions/transaction/pdf.html', {'transaction': transaction})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=transaction_{transaction_id}.pdf'
    weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response)
    return response


def export_to_csv(request, account_slug):
    target_account = get_object_or_404(Account, slug=account_slug)
    queryset = get_queryset(request).filter(account=target_account)
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
    # Data
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            data_row.append(value)
        writer.writerow(data_row)
    return response
