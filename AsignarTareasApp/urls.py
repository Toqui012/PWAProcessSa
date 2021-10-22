from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from AsignarTareasApp.views import AsignarTareaSection, AsignarTareaUsuarioSection, AssignTask
from LoginApp.views import logout

urlpatterns = [
    path('asignarTareaSection/', AsignarTareaSection, name="AsignarTareaSection"),
    path('asignarTareaUsuarioSection/<int:idTask>', AsignarTareaUsuarioSection, name="AsignarTareaUsuarioSection"),
    path('assignTaskProcedure/<str:idTask>/<str:rutUser>', AssignTask, name="AssignTaskProcedure"), 
    path('logout/', logout, name='logout'),
]