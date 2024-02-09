import csv
import datetime

from django.contrib import admin
from django.http import HttpResponse

from .models import Comission, Transaction
from  transactions.views import export_to_csv

class TransactionComissionInline(admin.TabularInline):
    model = Comission
    readonly_fields = ['kind', 'transfer', 'amount']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['agent', 'kind', 'amount', 'concept', 'timestamp']
    actions = [export_to_csv]
    inlines=[TransactionComissionInline]


@admin.register(Comission)
class ComissionAdmin(admin.ModelAdmin):
    list_display = ['kind', 'transfer', 'amount']
