import csv
import datetime

from django.contrib import admin
from django.http import HttpResponse

from .models import Comission, Transaction
from  transactions.views import export_to_csv

# def admin_export_csv(modeladmin, queryset):
#     return export_to_csv()


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['agent', 'kind', 'amount', 'concept', 'timestamp']
    actions = [export_to_csv]


@admin.register(Comission)
class ComissionAdmin(admin.ModelAdmin):
    pass
