from django.db import models


class Product(models.Model):
    class Type(models.TextChoices):
        ACCOUNT = "ACC", "Account"
        CARD = "CRD", "Card"

    title = models.CharField(max_length=250)
    subtitle = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    body = models.TextField()
    image = models.ImageField(upload_to="products/%Y/%m/%d/", blank=True)
    type = models.CharField(max_length=3, choices=Type.choices)

    def __str__(self):
        return f'Prodct: {self.title}'
