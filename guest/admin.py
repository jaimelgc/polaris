from django.contrib import admin
from guest.models import Product
from parler.admin import TranslatableAdmin

@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    list_display = ['title', 'subtitle', 'slug', 'body', 'image', 'type']
