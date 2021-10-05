from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from DashboardApp.views import DashboardMain
from LoginApp.views import logout

urlpatterns = [
    path('', DashboardMain, name='DashboardMain'),
    path('logout/', logout, name='logout'),
]