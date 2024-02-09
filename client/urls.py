from django.urls import include, path

from . import views

urlpatterns = [
    path('login/', views.user_login, name='user_login'),
    path('', include('django.contrib.auth.urls')),
    path('edit/', views.edit, name='edit'),  # edit_profile mejor nombre?
    path('register/', views.register, name='register'),
    path('', views.dashboard, name='dashboard'),
    path('<slug:account_slug>/', views.dashboard, name="dashboard_acc_detail"),
    path('account/create', views.create_account, name='create_account'),
    path('account/<slug:account_slug>/modify', views.modify_account, name='modify_account'),
    path('card/create', views.create_card, name='create_card'),
    path('card/<int:card_id>/modify', views.modify_card, name='modify_card'),
]
