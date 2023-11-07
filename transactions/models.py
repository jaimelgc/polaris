from django.db import models

from client.models import Account


class Transaction(models.Model):
    agent = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    concept = models.CharField(max_length=120)
    timestamp = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(Account, related_name='transactions', on_delete=models.CASCADE)
    # Falta kind

    def __str__(self):
        return f'Transaction {self.id} - {self.amount}'

    class Meta:
        indexes = [models.Index(fields=['-timestamp'])]
        ordering = ['-timestamp']
