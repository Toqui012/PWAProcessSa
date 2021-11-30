from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from DashboardApp.views import DashboardMain
from DashboardApp.views import UserSection
from DashboardApp.views import AddUserSection
from DashboardApp.views import DeleteUserSection
from DashboardApp.views import EditUserSection
from LoginApp.views import logout
from django.urls import reverse

urlpatterns = [
    path('', DashboardMain, name='DashboardMain'),
    path('userSection/', UserSection, name='UserSection'),
    path('addUserSection/', AddUserSection, name='AddUserSection'),
    path('userSection/deleteUserSection/<str:idUser>', DeleteUserSection, name = 'DeleteUserSection'),
    # path('userSection/updateUserSection/<str>:idUser>', EditUserSection, name = 'UpdateUserSection'),
    path('userSection/updateUserSection/<str:idUser>', EditUserSection, name = 'UpdateUserSection'),
    path('logout/', logout, name='logout'),
]