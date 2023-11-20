from django.contrib import admin

from .models import Account, Card, Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'avatar']
    raw_id_fields = ['user']


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['alias', 'balance', 'status', 'user', 'id']
    raw_id_fields = ['user']


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['alias', 'status', 'user', 'account']
    raw_id_fields = ['user', 'account']
