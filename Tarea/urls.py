from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from Tarea.views import AddTareaSection
from Tarea.views import TareaSection
#from DashboardApp.views import DashboardMain
#from DashboardApp.views import UserSection
#from DashboardApp.views import AddUserSection
from LoginApp.views import logout

urlpatterns = [
    path('tareaSection/', TareaSection, name='TareaSection'),
    path('addTareaSection/', AddTareaSection, name='AddTareaSection'),
    #path('readTareaSection/', ReadTareaSection, name='ReadTareaSection'),
    #path('updateTareaSection/', UpdateTareaSection, name='UpdateTareaSection'),
    #path('deleteTareaSection/', DeleteTareaSection, name='DeleteTareaSection'),
]