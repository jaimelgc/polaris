from rest_framework import serializers

from client.models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['alias', 'code', 'status', 'balance']
