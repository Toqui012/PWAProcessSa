from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from LoginApp.views import logout
from UnidadInternaApp.views import AddUnidadInternaSection, DeleteUnidadInternaSection, EditUnidadInternaSection, UnidadInternaSection

urlpatterns = [
    path('unidadInternaSection/', UnidadInternaSection, name='UnidadInternaSection'),
    path('addUnidadInternaSection/', AddUnidadInternaSection, name='AddUnidadInternaSection'),
    path('unidadInternaSection/deleteUnidadInternaSection/<int:idUnidadInterna>', DeleteUnidadInternaSection, name='DeleteUnidadInternaSection'),
    path('unidadInternaSection/updateUnidadInternaSection/<int:idUnidadInterna>', EditUnidadInternaSection, name='EditUnidadInternaSection'),
    path('logout/', logout, name='logout'),
]