# encoding:utf-8
from django.urls import path
from .views.base import Index
from .views.auth import Login

urlpatterns = [
    path('index/', Index.as_view(), name='index'),
    path('login/', Login.as_view(), name='login')
]
