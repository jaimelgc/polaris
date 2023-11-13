from django.urls import path

from . import views

urlpatterns = [
    path('', views.transfer, name='payments'),
    path('incoming/', views.transfer_inc, name='transfer_inc'),
]
