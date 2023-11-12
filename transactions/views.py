import json
from decimal import Decimal

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from client.models import Card

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
            card = Card.objects.filter(id=card_id, pin=data['pin'])[0]
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
        return HttpResponseBadRequest(data.keys())
