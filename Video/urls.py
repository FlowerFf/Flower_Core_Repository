# encoding:utf-8
from django.contrib import admin
from django.urls import path, include
from Video_app.client import urls as client_urls
from Video_app.dashboard import urls as dashboard_urls

urlpatterns = [
    path('dashboard/', include(dashboard_urls)),
    path('client/', include(client_urls))
]
