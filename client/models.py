from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class Client(models.Model):
    class States(models.TextChoices):
        ACTIVE = "AC", _("Active")
        BLOQUED = "BL", _("Bloqued")
        TERMINATED = "TE", _("Terminated")

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    status = models.CharField(max_length=2, choices=States.choices, default=States.ACTIVE)

    def __str__(self):
        return self.user.username


class Account(models.Model):
    class States(models.TextChoices):
        ACTIVE = "AC", _("Active")
        BLOQUED = "BL", _("Bloqued")
        TERMINATED = "TE", _("Terminated")

    alias = models.CharField(_("alias"), max_length=120)
    slug = models.SlugField(_("slug"), max_length=120, blank=True)
    balance = models.DecimalField(_("balance"), max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(_("status"), max_length=2, choices=States.choices, default='AC')
    user = models.ForeignKey(
        Client,
        related_name='accounts',
        on_delete=models.CASCADE,
        verbose_name=_("user"),
    )

    def __str__(self):
        return self.alias

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.alias)
        super().save(*args, **kwargs)

    @property
    def code(self):
        return f'A6-{str(self.id).zfill(4)}'

    def get_absolute_url(self):
        return reverse('dashboard_acc_detail', args=[self.slug])


class Card(models.Model):
    class States(models.TextChoices):
        ACTIVE = "AC", _("Active")
        BLOQUED = "BL", _("Bloqued")
        TERMINATED = "TE", _("Terminated")

    alias = models.CharField(_("alias"), max_length=120)
    status = models.CharField(
        _("status"), max_length=2, choices=States.choices, default=States.ACTIVE
    )
    pin = models.CharField(_("pin"), max_length=3)
    user = models.ForeignKey(
        Client,
        related_name='cards',
        on_delete=models.CASCADE,
        verbose_name=_("user"),
    )
    account = models.ForeignKey(
        Account,
        related_name='cards',
        on_delete=models.CASCADE,
        verbose_name=_("account"),
    )
    image = models.ImageField(
        _("image"),
        upload_to='card/%Y/%m/%d/',
        default="card.png",
        blank=True,
    )

    def __str__(self):
        return self.alias

    @property
    def code(self):
        return f'C6-{str(self.id).zfill(4)}'
