from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy

from LoginApp.views import authenticated, decodered
import requests, jwt, json

# librerias para hacer pdf
import os
from django.conf import settings
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa

from django.views.generic import TemplateView, View

# seccion para elgir el PDF a crear
def GrafictSection(request):
    if authenticated(request):
        token = request.COOKIES.get('validate')
        headers = {'Content-Type':'application/json', 'Authorization': 'Bearer '+ token}
        
        
        if request.method == 'POST':
            
            option = request.POST.get('grapichSelection')
            if option == 'tareas':
                return ReporteTarea(request)
            if option == 'empresas':
                return ReporteEmpresas(request)
            if option == 'usuario':
                return ReporteEmpleados(request)
            if option == 'tareaSubordinada':
                return ReporteTareaSubordinada(request)
            else:
                return HttpResponseRedirect(reverse_lazy('DashboardMain'))
        return render(request,'PDF/reporteSelection.html')


# reporte de tareas
def ReporteTarea(request):
    if authenticated(request):
        
        template = get_template('PDF/pdf_tareas.html')
        # Consumo de API: Usuario
        # Method: GET
        token = request.COOKIES.get('validate')
        headers = {'Content-Type':'application/json', 'Authorization': 'Bearer '+ token}
        req = requests.get('http://localhost:32482/api/tarea', headers=headers)
        dataAPI = req.json()
        listTarea = dataAPI['data']
        
        #Variables con data a enviar a la vista
        context = {
            'tareas': listTarea,
            'name':'Tareas'
        }
        # Return Section
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        pisaStatus = pisa.CreatePDF(
            html, dest=response
        )
        print(response)
        if pisaStatus.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
    else:
        return HttpResponseRedirect(reverse_lazy('DashboardMain'))


# reporte Empleados
def ReporteEmpleados(request):
    if authenticated(request):
        
        template = get_template('PDF/pdf_empleados.html')
        # Consumo de API: Usuario
        # Method: GET
        token = request.COOKIES.get('validate')
        headers = {'Content-Type':'application/json', 'Authorization': 'Bearer '+ token}
        req = requests.get('http://localhost:32482/api/usuario', headers=headers)
        dataAPI = req.json()
        listTarea = dataAPI['data']
        
        #Variables con data a enviar a la vista
        
        context = {
            'empleados': listTarea,
            'name':'Empleados'
        }
        # Return Section
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        pisaStatus = pisa.CreatePDF(
            html, dest=response
        )
        print(response)
        if pisaStatus.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
    else:
        return HttpResponseRedirect(reverse_lazy('DashboardMain'))


# Reporte Tareas Subordinadas
def ReporteTareaSubordinada(request, *args, **kwargs):
    if authenticated(request):
        template = get_template('PDF/pdf_tarea_subordinada.html')
        # Consumo de API: Tareas Subordinadas
        # Method: GET
        token = request.COOKIES.get('validate')
        headers = {'Content-Type':'application/json', 'Authorization': 'Bearer '+ token}
        req = requests.get('http://localhost:32482/api/TareaSubordinada', headers=headers)
        dataAPI = req.json()
        listTareaSubordinada = dataAPI['data']
        #Variables con data a enviar a la vista
        context = {
            'tareasSubordinadas': listTareaSubordinada,
            'name':'Tareas Subordinadas'
        }
        # Return Section
        html = template.render(context)
        # Comentar la línea de abajo para que no se descargue automático
        response = HttpResponse(content_type='application/pdf')
        #response['Content-Disposition'] = 'attachment; filename="reporte_tarea_subordinada.pdf"'
        pisaStatus = pisa.CreatePDF(
            html, dest=response
        )
        if pisaStatus.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
    else:
        return HttpResponseRedirect(reverse_lazy('DashboardMain'))   


# reporte Empresas 
def ReporteEmpresas(request, *args, **kwargs):
    if authenticated(request):
        template = get_template('PDF/pdf_empresas.html')
        # Consumo de API: Empresas
        # Method: GET
        token = request.COOKIES.get('validate')
        headers = {'Content-Type':'application/json', 'Authorization': 'Bearer '+ token}
        req = requests.get('http://localhost:32482/api/business', headers=headers)
        dataAPI = req.json()
        listEmpresas = dataAPI['data']
        #Variables con data a enviar a la vista
        context = {
            'empresas': listEmpresas,
            'name':'Empresas'
        }
        # Return Section
        html = template.render(context)
        # Comentar la línea de abajo para que no se descargue automático
        response = HttpResponse(content_type='application/pdf')
        #response['Content-Disposition'] = 'attachment; filename="reporte_empresa.pdf"'
        pisaStatus = pisa.CreatePDF(
            html, dest=response
        )
        if pisaStatus.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
    else:
        return HttpResponseRedirect(reverse_lazy('DashboardMain'))
























# Clase para pdf TEST
class TestPDF(TemplateView):
    def get(self, request, *args, **kwargs):
        if authenticated(request):
            template = get_template('PDF/invoice.html')
            # Consumo de API: Tareas
            # Method: GET
            token = request.COOKIES.get('validate')
            headers = {'Content-Type':'application/json', 'Authorization': 'Bearer '+ token}
            req = requests.get('http://localhost:32482/api/tarea', headers=headers)
            dataAPI = req.json()
            listTarea = dataAPI['data']
            #Variables con data a enviar a la vista
            context = {
                'tareas': listTarea
            }
            # Return Section
            html = template.render(context)
            # Comentar la línea de abajo para que no se descargue automático
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="reporte_tarea.pdf"'
            pisaStatus = pisa.CreatePDF(
                html, dest=response
            )
            if pisaStatus.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            print(response)
            return response
        else:
            return HttpResponseRedirect(reverse_lazy('DashboardMain'))


# Sección para todos los PDF
def PDFSection(request):
    return render(request, 'PDF/pdf_general.html')
