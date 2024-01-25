from django.contrib import admin
from guest.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'subtitle', 'slug', 'body', 'image', 'type']
    prepopulated_fields = {"slug": ["title",]}
