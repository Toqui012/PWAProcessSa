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
            return response
        else:
            return HttpResponseRedirect(reverse_lazy('DashboardMain'))







        # try:
        #     #obtengo el template que va hacer de base para hacer el pdf
        #     template = get_template('invoice.html')
        #     #creo un diccionario context con las vriable que voy a usar y lo envio con render
        #     print('okey')
        #     token = request.COOKIES.get('validate')
        #     headers = {'Content-Type':'application/json', 'Authorization': 'Bearer '+ token}
        #     req = requests.get('http://localhost:32482/api/tarea', headers=headers)
        #     dataAPI = req.json()
        #     listTarea = dataAPI['data']
            
        #     context = {
        #         'tareas':listTarea,
        #         'tittle':'hola'
        #     }
        #     html = template.render(context)
            
        #     #se crea el pdf y se descarga
        #     response = HttpResponse(content_type='application/pdf')
        #     #response['Content-Disposition'] = 'attachment; filename="report.pdf"' # esto hace que el pdf se descargue directamente

        #     # llama a la libreria xhtml2pdf para crear el pdf
        #     pisaStatus = pisa.CreatePDF(
        #         html, dest=response
        #     )
        #     if pisaStatus.err:
        #         return HttpResponse('We had some errors <pre>' + html + '</pre>')
        #     return response
        # except:
        #     pass
        # return HttpResponseRedirect(reverse_lazy('DashboardMain'))




