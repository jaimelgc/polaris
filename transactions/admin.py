from django.contrib import admin

from .models import Comission, Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    pass


@admin.register(Comission)
class ComissionAdmin(admin.ModelAdmin):
    pass
