from django.urls import path
from django.utils.translation import gettext_lazy as _

from . import views

urlpatterns = [
    path('', views.transfer, name='payments'),
    path(_('incoming/'), views.transfer_inc, name='transfer_inc'),
    path(_('outgoing/'), views.transfer_out, name='transfer_out'),
    path(_('client/<slug:account_slug>/'), views.export_to_csv, name='export_to_csv'),
    path('<int:id>/', views.transfer_detail, name='transfer_detail'),
    path('<int:transaction_id>/pdf/', views.transaction_pdf, name='transaction_pdf'),
]
