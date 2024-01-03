from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse

from client.models import Account


class Transaction(models.Model):
    class Type(models.TextChoices):
        INCOMING = "INC", "Incomming"
        OUTGOING = "OUT", "Outgoing"
        PAYMENT = "PAY", "Payment"

    agent = models.CharField(max_length=120)
    amount = models.DecimalField(
        validators=[MinValueValidator(Decimal('0.01'))], max_digits=10, decimal_places=2
    )
    concept = models.CharField(max_length=120, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(Account, related_name='transactions', on_delete=models.CASCADE)
    kind = models.CharField(max_length=3, choices=Type.choices)

    def __str__(self):
        return f'Transaction {self.id} - {self.amount}'

    class Meta:
        indexes = [models.Index(fields=['-timestamp'])]
        ordering = ['-timestamp']

    def get_absolute_url(self):
        return reverse('transfer_detail', args=[self.id])


class Comission(models.Model):
    class Type(models.TextChoices):
        INCOMING = "INC", "Incomming Transaction"
        OUTGOING = "OUT", "Outgoing Transaction"
        PAYMENT = "PAY", "Payment"

    kind = models.CharField(max_length=3, choices=Type.choices)
    transfer = models.ForeignKey(Transaction, related_name='comissions', on_delete=models.CASCADE)
    amount = models.DecimalField(
        MinValueValidator(Decimal('0.01')), decimal_places=2, max_digits=10
    )
