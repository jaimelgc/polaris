from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Transaction


class TransactionForm(forms.ModelForm):
    account = forms.CharField(label=_('Recipient'), max_length=120)

    class Meta:
        model = Transaction
        fields = ['concept', 'amount', 'agent']
