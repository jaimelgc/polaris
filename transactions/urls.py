from django.urls import path

from . import views

urlpatterns = [
    path('', views.transfer, name='payments'),
    path('incoming/', views.transfer_inc, name='transfer_inc'),
    path('outgoing/', views.transfer_out, name='transfer_out'),
    path(
        'movements/<int:account_id>/', views.TransactionListView.as_view(), name='account_movements'
    ),
    path('client/#', views.export_to_csv, name='export_to_csv'),
    path('movements/', views.TransactionListView.as_view(), name='movements'),
    path('<int:id>/', views.transfer_detail, name='transfer_detail'),
    path('<int:transaction_id>/pdf/', views.transaction_pdf, name='transaction_pdf'),
]
