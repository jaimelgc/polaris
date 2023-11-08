from django.urls import include, path

from . import views

app_name = 'client'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
]
