from django.contrib.auth import views as auth_views
from django.urls import include, path

from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done',
    ),
    path(
        'password-reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm',
    ),
    path(
        'password-reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete',
    ),
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path(
        'password-change/done/',
        auth_views.PasswordChangeDoneView.as_view(),
        name='password_change_done',
    ),
    path('', views.dashboard, name='dashboard'),
    path('edit/', views.edit, name='edit'),
    path('edit/done', views.edit, name='edit_done'),
    path('account/create', views.create_account, name='create_account'),
    path('card/create', views.create_card, name='create_card'),
    path('card/done', views.create_card, name='card_done'),
    path('account/done', views.create_account, name='account_done'),
    path('<slug:account_slug>/', views.dashboard, name="dashboard_acc_detail"),
]
