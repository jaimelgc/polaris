from django.urls import include, path
from django.utils.translation import gettext_lazy as _

from . import views

urlpatterns = [
    path(_('login/'), views.user_login, name='user_login'),
    path('', include('django.contrib.auth.urls')),
    path(_('edit/'), views.edit, name='edit'),  # edit_profile mejor nombre?
    path(_('register/'), views.register, name='register'),
    path('', views.dashboard, name='dashboard'),
    path('<slug:account_slug>/', views.dashboard, name="dashboard_acc_detail"),
    path(_('account/create'), views.create_account, name='create_account'),
    path(_('account/<slug:account_slug>/modify'), views.modify_account, name='modify_account'),
    path(_('card/create'), views.create_card, name='create_card'),
    path(_('card/<int:card_id>/modify'), views.modify_card, name='modify_card'),
]
