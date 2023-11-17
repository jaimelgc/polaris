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
        print(self.cleaned_data['agent'])

    class Meta:
        model = Transaction
        fields = ['concept', 'amount', 'agent']
