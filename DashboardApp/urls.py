from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.DashboardMain, name='DashboardMain')
]