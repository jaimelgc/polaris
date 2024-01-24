from django.urls import path

from . import views

urlpatterns = [
    path(
        'accounts/',
        views.AccountListView.as_view(),
        name='accounts_list',
    ),
]
