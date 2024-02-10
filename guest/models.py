from django.db import models
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    class Type(models.TextChoices):
        ACCOUNT = "ACC", _("Account")
        CARD = "CRD", _("Card")

    title = models.CharField(_('title'), max_length=250)
    subtitle = models.CharField(_('subtitle'), max_length=250)
    slug = models.SlugField(max_length=250)
    body = models.TextField(_('body'))
    image = models.ImageField(_('image'), upload_to="products/%Y/%m/%d/", blank=True)
    type = models.CharField(_('type'), max_length=3, choices=Type.choices)

    def __str__(self):
        static_text = _('Product: ')
        return f'{static_text}{self.title}'
