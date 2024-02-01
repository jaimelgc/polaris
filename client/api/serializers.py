from rest_framework import serializers

from client.models import Account, Card
from transactions.models import Comission, Transaction


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['alias', 'code', 'status', 'balance']


class ComissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comission
        fields = ['kind', 'amount']


class TransactionSerializer(serializers.ModelSerializer):
    comissions = ComissionSerializer(many=True, read_only=True)

    class Meta:
        model = Transaction
        fields = [
            'agent',
            'kind',
            'amount',
            'concept',
            'timestamp',
            'comissions',
        ]


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = [
            'alias',
            'status',
            'pin',
            'account',
            'image',
        ]
