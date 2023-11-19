from django import forms

from .models import Transaction


class TransactionForm(forms.ModelForm):
    account = forms.CharField(label='Recipient', max_length=120)

    class Meta:
        model = Transaction
        fields = ['concept', 'amount', 'agent']
