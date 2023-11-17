from django import forms
from django.core.exceptions import ValidationError

from .models import Transaction


class TransactionForm(forms.ModelForm):
    account = forms.CharField(label='cuenta de destino', max_length=120)

    # campo dirección para probar
    def clean_amount(self):
        '''
            Comprobamos que haya dinero suficiente en la cuenta elegida para realizar la operación
        '''
        data = self.cleaned_data['amount']
        balance = self.cleaned_data['agent']
        if data > balance.balance:
            raise ValidationError('You don’t have enough money in this account')

    class Meta:
        model = Transaction
        fields = ['concept', 'amount', 'agent']
