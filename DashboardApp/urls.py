from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from DashboardApp.views import DashboardMain
from DashboardApp.views import UserSection
from LoginApp.views import logout

urlpatterns = [
    path('', DashboardMain, name='DashboardMain'),
    path('userSection/', UserSection, name='UserSection'),
    path('logout/', logout, name='logout'),
]