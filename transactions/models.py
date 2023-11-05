from django.conf import settings
from django.db import models


class Transaction(models.Model):
    agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    concept = models.CharField(max_length=120)
    timestamp = models.DateTimeField(auto_now_add=True)
    # Falta kind

    def __str__(self):
        return f'Transaction {self.id} - {self.amount}'

    class Meta:
        indexes = [models.Index(fields=['-timestamp'])]
        ordering = ['-timestamp']


class Agent(models.Model):
    name = models.CharField(max_length=50)
