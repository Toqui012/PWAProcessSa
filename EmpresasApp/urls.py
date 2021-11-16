from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from EmpresasApp.views import AddEmpresaSection, DeleteEmpresaSection, EditEmpresaSection, EmpresaSection
from LoginApp.views import logout

urlpatterns = [
    path('empresaSection/', EmpresaSection, name='EmpresaSection'),
    path('addEmpresaSection/', AddEmpresaSection, name='AddEmpresaSection'),
    path('empresaSection/deleteEmpresaSection/<str:rutEmpresa>', DeleteEmpresaSection, name='DeleteEmpresaSection'),
    path('empresaSection/updateEmpresaSection/(?P<rutEmpresa>[0-9]+)$', EditEmpresaSection, name='UpdateEmpresaSection'),
    path('logout/', logout, name='logout'),
]