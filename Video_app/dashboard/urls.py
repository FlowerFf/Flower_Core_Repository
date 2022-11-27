# encoding:utf-8
from django.urls import path
from .views.base import Index
from .views.auth import Login, AdminManager, LoginOut, AminManagerUpdateStatus

urlpatterns = [
    path('index/', Index.as_view(), name='index'),
    path('login/', Login.as_view(), name='login'),
    path('adminManager/', AdminManager.as_view(), name='manager'),
    path('loginout/', LoginOut.as_view(), name='logout'),
    path('updatestatus/', AminManagerUpdateStatus.as_view(), name='update')
]
