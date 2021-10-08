from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from LoginApp.views import logout
from TareaSubordinada.views import AddTareaSubordinadaSection, TareaSubordinadaSection

urlpatterns = [
    path('tareaSubordinadaSection/', TareaSubordinadaSection, name='TareaSubordinadaSection'),
    path('addTareaSubordinadaSection/', AddTareaSubordinadaSection, name="AddTareaSubordinadaSection"),
    path('logout/', logout, name='logout'),
]