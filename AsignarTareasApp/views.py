from json import dump
from django.http.request import HttpRequest
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.context_processors import request
from requests.api import head
from LoginApp.views import authenticated, decodered
import requests, jwt, json


# Create your views here.

def AsignarTareaSection(request):
    print("Hello world :D")
    return render(request, 'Asignar_Tarea/asignar_tarea.html')

def AsignarTareaUsuarioSection(request):
    if authenticated(request):
        # Return Section
        token = request.COOKIES.get('validate')
        headers = {'Content-Type':'application/json', 'Authorization': 'Bearer '+ token}
        reqUsers = requests.get('http://localhost:32482/api/usuario', headers=headers)
        dataAPI = reqUsers.json()
        listUsers = dataAPI['data']

        # Variables con data a enviar a la vista
        context = {
            'users': listUsers
        }

        return render(request, 'Asignar_Tarea/list_user_asignar.html', {'data': context})
    