from django.conf import settings
from django.db import models


class Client(models.Model):
    class States(models.TextChoices):
        ACTIVE = "AC", "Active"
        BLOQUED = "BL", "Bloqued"
        TERMINATED = "TE", "Terminated"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # username = models.CharField(max_length=50)
    # first_name = models.CharField(max_length=50)
    # last_name = models.CharField(max_length=50)
    # email = models.EmailField()
    avatar = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    status = models.CharField(max_length=2, choices=States.choices, default=States.ACTIVE)

    def __str__(self):
        return self.user.username


class Account(models.Model):
    class States(models.TextChoices):
        ACTIVE = "AC", "Active"
        BLOQUED = "BL", "Bloqued"
        TERMINATED = "TE", "Terminated"

    alias = models.CharField(max_length=120)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=2, choices=States.choices)
    user = models.ForeignKey(
        Client,
        related_name='accounts',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.alias

    @property
    def code(self):
        return f'A6-{str(self.id).zfill(4)}'


class Card(models.Model):
    class States(models.TextChoices):
        ACTIVE = "AC", "Active"
        BLOQUED = "BL", "Bloqued"
        TERMINATED = "TE", "Terminated"

    alias = models.CharField(max_length=120)
    status = models.CharField(max_length=2, choices=States.choices, default=States.ACTIVE)
    pin = models.CharField(max_length=3)
    user = models.ForeignKey(Client, related_name='cards', on_delete=models.CASCADE)
    account = models.ForeignKey(Account, related_name='cards', on_delete=models.CASCADE)

    def __str__(self):
        return self.alias

    @property
    def code(self):
        return f'C6-{str(self.id).zfill(4)}'
