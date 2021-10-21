from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from AsignarTareasApp.views import AsignarTareaSection, AsignarTareaUsuarioSection
from LoginApp.views import logout

urlpatterns = [
    path('asignarTareaSection/', AsignarTareaSection, name="AsignarTareaSection"),
    path('asignarTareaUsuarioSection/', AsignarTareaUsuarioSection, name="AsignarTareaUsuarioSection"), 
    path('logout/', logout, name='logout'),
]