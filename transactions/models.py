from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from client.models import Account


class Transaction(models.Model):
    class Type(models.TextChoices):
        INCOMING = "INC", _("Incomming")
        OUTGOING = "OUT", _("Outgoing")
        PAYMENT = "PAY", _("Payment")

    agent = models.CharField(_("agent"), max_length=120)
    amount = models.DecimalField(
        verbose_name=_("amount"),
        validators=[MinValueValidator(Decimal('0.01'))],
        max_digits=10,
        decimal_places=2,
    )
    concept = models.CharField(_("concept"), max_length=120, blank=True)
    timestamp = models.DateTimeField(_("timestamp"), auto_now_add=True)
    account = models.ForeignKey(
        Account,
        related_name='transactions',
        on_delete=models.CASCADE,
        verbose_name="account",
    )
    kind = models.CharField(
        _("kind"),
        max_length=3,
        choices=Type.choices,
    )

    def __str__(self):
        return f'Transaction {self.id} - {self.amount}'

    class Meta:
        indexes = [models.Index(fields=['-timestamp'])]
        ordering = ['-timestamp']

    def get_absolute_url(self):
        return reverse('transfer_detail', args=[self.id])


class Comission(models.Model):
    class Type(models.TextChoices):
        INCOMING = "INC", _("Incomming Transaction")
        OUTGOING = "OUT", _("Outgoing Transaction")
        PAYMENT = "PAY", _("Payment")

    kind = models.CharField(
        max_length=3,
        choices=Type.choices,
        verbose_name=_("kind"),
    )
    transfer = models.ForeignKey(
        Transaction,
        related_name='comissions',
        on_delete=models.CASCADE,
        verbose_name=_(
            "transfer",
        ),
    )
    amount = models.DecimalField(
        MinValueValidator(Decimal('0.01')),
        decimal_places=2,
        max_digits=10,
        verbose_name=_("amount"),
    )
