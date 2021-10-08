from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from DashboardApp.views import DashboardMain
from DashboardApp.views import UserSection
from DashboardApp.views import AddUserSection
from DashboardApp.views import DeleteUserSection
from LoginApp.views import logout

urlpatterns = [
    path('', DashboardMain, name='DashboardMain'),
    path('userSection/', UserSection, name='UserSection'),
    path('addUserSection/', AddUserSection, name='AddUserSection'),
    path('userSection/deleteUserSection/<str:idUser>', DeleteUserSection, name = 'DeleteUserSection'),
    path('logout/', logout, name='logout'),
]