from django.shortcuts import render
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
# Create your views here.

def GrafictSection(request):
    if authenticated(request):
        token = request.COOKIES.get('validate')
        headers = {'Content-Type':'application/json', 'Authorization': 'Bearer '+ token}
        
        
        if request.method == 'POST':
            
            option = request.POST.get('grapichSelection')
            if option == 'tareas':
                return graphicTarea(request)
            if option == 'usuario':
                return graphicUsuario(request)
            else:
                return HttpResponseRedirect(reverse_lazy('DashboardMain'))
        return render(request,'graphicSelection.html')


def graphicTarea(request):
    if authenticated(request):
        
        template = get_template('Template_informe/tareas.html')
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


def graphicUsuario(request):
    if authenticated(request):
        
        template = get_template('invoice.html')
        # Consumo de API: Usuario
        # Method: GET
        token = request.COOKIES.get('validate')
        headers = {'Content-Type':'application/json', 'Authorization': 'Bearer '+ token}
        req = requests.get('http://localhost:32482/api/usuario', headers=headers)
        dataAPI = req.json()
        listTarea = dataAPI['data']
        
        #Variables con data a enviar a la vista
        context = {
            'tareas': listTarea,
            'name':'Usuario'
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



class TestPDF(TemplateView):
    def get(self, request, *args, **kwargs):
        if authenticated(request):
            template = get_template('invoice.html')
            # Consumo de API: Usuario
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
            response = HttpResponse(content_type='application/pdf')
            #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            pisaStatus = pisa.CreatePDF(
                html, dest=response
            )
            if pisaStatus.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            print(response)
            return response
        else:
            return HttpResponseRedirect(reverse_lazy('DashboardMain'))




