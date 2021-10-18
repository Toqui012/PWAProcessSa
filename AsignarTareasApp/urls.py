from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from AsignarTareasApp.views import AsignarTareaSection
from LoginApp.views import logout
#from TareaSubordinada.views import 

urlpatterns = [
    path('asignarTareaSection/', AsignarTareaSection, name="AsignarTareaSection"),
    path('logout/', logout, name='logout'),
]