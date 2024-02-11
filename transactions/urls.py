from django.urls import path
from django.utils.translation import gettext_lazy as _

from . import views

urlpatterns = [
    path('', views.transfer, name='payments'),
    path(_('incoming/'), views.transfer_inc, name='transfer_inc'),
    path(_('outgoing/'), views.transfer_out, name='transfer_out'),
    path(
        _('movements/<int:account_id>/'),
        views.TransactionListView.as_view(),
        name='account_movements',
    ),
    path(_('client/#'), views.export_to_csv, name='export_to_csv'),
    path(_('movements/'), views.TransactionListView.as_view(), name='movements'),
    path('<int:id>/', views.transfer_detail, name='transfer_detail'),
    path('<int:transaction_id>/pdf/', views.transaction_pdf, name='transaction_pdf'),
]
