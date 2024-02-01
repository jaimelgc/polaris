from django.urls import path

from . import views

urlpatterns = [
    path(
        'accounts/',
        views.AccountListView.as_view(),
        name='accounts_list',
    ),
    path(
        'accounts/<pk>/',
        views.AccountDetailView.as_view(),
        name='account_detail',
    ),
    path(
        'transactions/',
        views.TransactionListView.as_view(),
        name='transactions_list',
    ),
    path(
        'transactions/<pk>/',
        views.TransactionDetailView.as_view(),
        name='transaction_detail',
    ),
]
