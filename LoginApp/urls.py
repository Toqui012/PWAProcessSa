from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from LoginApp import views

urlpatterns = [
    path('', views.login, name='login'),
    path('validate',views.validate, name='validate'),
]