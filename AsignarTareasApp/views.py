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
        token = request.COOKIES.get('validatepwa')
        headers = {'Content-Type':'application/json', 'Authorization': 'Bearer '+ token}
        reqTask = requests.get('http://localhost:32482/api/tarea/', headers=headers)
        dataAPI = reqTask.json()
        listTask = dataAPI['data']
        
        reqUser = requests.get('http://localhost:32482/api/usuario', headers=headers)
        dataAPIUser = reqUser.json()
        listUser = dataAPIUser['data']
        
        # recopilacion de Rut Usuario authenticado
        test = decodered(token)
        print(test['nameid'])
        
        #Codigo Filtrado
        filtroUnidadInterna = None
        
        for i in listUser:
                if test['nameid'] == i['rutUsuario']: 
                    filtroUnidadInterna = i['idUnidadInternaUsuario']
                    
        reqFiltroTarea = requests.get('http://localhost:32482/api/tarea/getTaskByBusiness/'+ str(filtroUnidadInterna), headers=headers)
        dataAPIFiltrado = reqFiltroTarea.json()
        listaFiltrada = dataAPIFiltrado['data']

        context = {
            'task': listaFiltrada,
            'rutUsuarioLogeado': test['nameid'] 
        }

        # Return Section
        return render(request, 'Asignar_Tarea/asignar_tarea.html',{'data': context})
    else:
        redirect('login')

# Función encargada de asignar una tarea a un usuario
def AsignarTareaUsuarioSection(request, idTask):
    if authenticated(request):
        token = request.COOKIES.get('validatepwa')
        headers = {'Content-Type':'application/json', 'Authorization': 'Bearer '+ token}
        reqUsers = requests.get('http://localhost:32482/api/usuario', headers=headers)
        dataAPI = reqUsers.json()
        listUsers = dataAPI['data']
        
        
        # Prueba de test
        test = decodered(token)
        print(test['nameid'])
        
        #Codigo Filtrado
        filtroUnidadInterna = None
        
        for i in listUsers:
            if test['nameid'] == i['rutUsuario']: 
                filtroUnidadInterna = i['idUnidadInternaUsuario']
                
        reqFiltroUsuario = requests.get('http://localhost:32482/api/tarea/getUserByBusiness/'+ str(filtroUnidadInterna), headers=headers)
        dataAPIFiltrado = reqFiltroUsuario.json()
        listaFiltrada = dataAPIFiltrado['data']
        
        # Variables con data a enviar a la vista
        context = {
            'users': listaFiltrada,
            'idTask': idTask,
            'rutUsuarioLogeado': test['nameid']
        }

        # Return Section
        return render(request, 'Asignar_Tarea/list_user_asignar.html', {'data': context})
    else:
        redirect('login')

def AssignTask(request, idTask, rutUser):
    if authenticated(request):
        try:
            token = request.COOKIES.get('validatepwa')
            headers = {'Accept-Encoding': 'UTF-8', 'Content-Type': 'application/json', 'Authorization': 'Bearer '+ token,'Accept': '*/*' }
            reqAssignTask = requests.put('http://localhost:32482/api/tarea/assignTask/'+ idTask + '/' + rutUser , headers=headers)
            print(reqAssignTask)
            return redirect('AsignarTareaSection')
        except:
            print('no funciona')

    else:
        redirect('login')
        



