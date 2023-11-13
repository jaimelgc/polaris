import json
from decimal import Decimal

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from client.models import Account, Card

from .models import Transaction


@csrf_exempt
def transfer(request):
    # request.body contiene el json con los datos
    data = json.loads(request.body)
    # En data tendremos un diccionario con los datos enviados
    if ['business', 'ccc', 'pin', 'amount'] == [key for key in data.keys()]:
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
        # comprobar que haya dinero para realizar cobro
        if amount < 0 and abs(amount) > account.balance:
            return HttpResponseBadRequest('No es posible realizar la operación')
        else:
            account.balance = account.balance + amount
            new_transaction = Transaction(
                agent=data['sender'],
                amount=data['amount'],
                concept=data['concept'],
                account=account,
                kind='INC',
            )
            account.save()
            new_transaction.save()
        return HttpResponse()
    else:
        return HttpResponseBadRequest('Los datos de la operación son incorrectos')
