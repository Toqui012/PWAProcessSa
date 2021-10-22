from json import dump
from django.http.request import HttpRequest
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.context_processors import request
from requests.api import head
from LoginApp.views import authenticated, decodered
import requests, jwt, json


# Create your views here.

# Función encargada de mostrar el listado de tareas disponibles a asignar
def AsignarTareaSection(request):
    if authenticated(request):
        token = request.COOKIES.get('validate')
        headers = {'Content-Type':'application/json', 'Authorization': 'Bearer '+ token}
        reqTask = requests.get('http://localhost:32482/api/tarea/', headers=headers)
        dataAPI = reqTask.json()
        listTask = dataAPI['data']

        context = {
            'task': listTask
        }

        # Return Section
        return render(request, 'Asignar_Tarea/asignar_tarea.html',{'data': context})
    else:
        redirect('login')

# Función encargada de asignar una tarea a un usuario
def AsignarTareaUsuarioSection(request, idTask):
    if authenticated(request):
        token = request.COOKIES.get('validate')
        headers = {'Content-Type':'application/json', 'Authorization': 'Bearer '+ token}
        reqUsers = requests.get('http://localhost:32482/api/usuario', headers=headers)
        dataAPI = reqUsers.json()
        listUsers = dataAPI['data']
        # Variables con data a enviar a la vista
        context = {
            'users': listUsers,
            'idTask': idTask
        }

        # Return Section
        return render(request, 'Asignar_Tarea/list_user_asignar.html', {'data': context})
    else:
        redirect('login')

def AssignTask(request, idTask, rutUser):
    if authenticated(request):
        try:
            token = request.COOKIES.get('validate')
            headers = {'Accept-Encoding': 'UTF-8', 'Content-Type': 'application/json', 'Authorization': 'Bearer '+ token,'Accept': '*/*' }
            reqAssignTask = requests.put('http://localhost:32482/api/tarea/assignTask/'+ idTask + '/' + rutUser , headers=headers)
            print(reqAssignTask)
            return redirect('AsignarTareaSection')
        except:
            print('no funciona')

    else:
        redirect('login')
        



