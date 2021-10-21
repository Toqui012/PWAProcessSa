from json import dump
from django.http.request import HttpRequest
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.context_processors import request
from requests.api import head
from LoginApp.views import authenticated, decodered
import requests, jwt, json

# Create your views here

def TareaSubordinadaSection(request):
    if authenticated(request):
        # Return Section
        token = request.COOKIES.get('validate')
        headers = {'Content-Type':'application/json', 'Authorization': 'Bearer '+ token}
        req = requests.get('http://localhost:32482/api/TareaSubordinada', headers=headers)
        dataAPI = req.json()
        listTareaSubordinada = dataAPI['data']

        #Variables con data a enviar a la vista
        context = {
            'tareaSubordinada': listTareaSubordinada
        }

        return render(request, 'Tarea_Subordinada/list_tarea_subordinada.html', {'data': context})

def AddTareaSubordinadaSection(request):
    if authenticated(request):
        # Consumo de API: Tarea
        # Method: GET
        token = request.COOKIES.get('validate')
        headers = {'Content-Type':'application/json', 'Authorization': 'Bearer '+ token}
        resTarea = requests.get('http://localhost:32482/api/tarea', headers=headers)
        dataTarea = resTarea.json()
        listTarea = dataTarea['data']

        # Consumo de API: Tarea Subordinada
        nombre = request.POST.get('nombreTareaSubordinada')
        descripcion = request.POST.get('descripcionTareaSubordinada')
        prioridadFk = request.POST.get('selectPrioridadTarea')
        estadoFk = request.POST.get('selectEstadoTarea')
        tareaFk = request.POST.get('selectTarea')

        status = ''
        if nombre == '' or descripcion == '' or prioridadFk == '' or estadoFk == '' or tareaFk == '' or nombre == None:
            status = 'ERROR'
        elif nombre != '' or descripcion != '' or prioridadFk != '' or estadoFk != '' or tareaFk != '' or nombre != None:
            status = 'OK'
        else: 
            status
        
        if status == 'OK':
             AddTareaSubordinada(request,nombre,descripcion,prioridadFk,estadoFk,tareaFk)

        # Variables con data para enviar a la vista
        context = {
            'tarea': listTarea,
            'statusCreation': status,
        }

        # Return Section
        return render(request, 'Tarea_Subordinada/tareaSubordinada.html', {'data': context})

    else:
        return redirect('login')

def DeleteTareaSubordinadaSection(request, idTareaSub):
    if authenticated:
        status = 'NO_CONTENT'
        token = request.COOKIES.get('validate')
        headers = {'Accept-Encoding': 'UTF-8', 'Content-Type': 'application/json', 'Authorization': 'Bearer '+ token,'Accept': '*/*' }

        # Consumo de API: Tarea Subordinada
        # Method: DELETE
        tareaSub = str(idTareaSub)
        payload = json.dumps({'idTareaSubordinada': tareaSub})
        r = requests.delete('http://localhost:32482/api/TareaSubordinada/delete/' + tareaSub, headers=headers, data=payload)
        print(r)

        # Consumo de API: Tarea Subordinada
        # Method: GET
        reqTareaSubordinada = requests.get('http://localhost:32482/api/TareaSubordinada', headers=headers)
        dataAPI = reqTareaSubordinada.json()
        listTareaSubordinada = dataAPI['data']

        context = {
            'tareaSubordinada': listTareaSubordinada,
            'deleteStatus': status
        }

        if r.ok:
            status = 'DELETED'
            print(status)
            return redirect('TareaSubordinadaSection')
        else: 
            status = 'ERROR'
            print(status)
            return render(request, 'Tarea_Subordinada/list_tarea_subordinada.html', {'data': context})
        
    else:
        return redirect('login')


def EditTareaSubordinadaSection(request, idTareaSub):
    if authenticated:

        # Configuración Header
        status = 'NO_CONTENT'
        token = request.COOKIES.get('validate')
        headers = {'Accept-Encoding': 'UTF-8', 'Content-Type': 'application/json', 'Authorization': 'Bearer '+ token,'Accept': '*/*' }

        # Consumo de API: Tarea
        # Method: GET
        resTarea = requests.get('http://localhost:32482/api/tarea', headers=headers)
        dataTarea = resTarea.json()
        listTarea = dataTarea['data']

        # Consumo de API: OneTareaSubordinada
        # Method: GET with Params
        tareaSub = str(idTareaSub)
        resOneTareaSub = requests.get('http://localhost:32482/api/TareaSubordinada/oneTareaSubordinada/'+ tareaSub, headers=headers)
        dataTareaSub = resOneTareaSub.json()
        OneTareaSubordinada = dataTareaSub['data']

        # Asignación del ID de Tarea Subordinada a Buscar
        idTareaSubordinadaToSearch = ''
        for x in OneTareaSubordinada:
            idTareaSubordinadaToSearch = x['idTareaSubordinada']
           # print(idTareaSubordinadaToSearch)

        # Validate Data Extraction
        if request.method == 'POST':
            try:
                #Recuperación de data proveniente del HTML
                nombre = request.POST.get('nombreTareaSubordinada')
                descripcion = request.POST.get('descripcionTareaSubordinada')
                prioridadFk = request.POST.get('selectPrioridadTarea')
                estadoFk = request.POST.get('selectEstadoTarea')
                tareaFk = request.POST.get('selectTarea')
                status = 'OK'
                #print(nombre, descripcion, tareaFk)
            except:
                status = 'ERROR'

        # Método Update User
        try:
            if status == 'OK':
                EditTareaSubordinada(request, nombre, descripcion, prioridadFk, estadoFk, tareaFk, idTareaSubordinadaToSearch)
            
        except:
            status = 'ERROR'
        
        context = {
            'tarea': listTarea,
            'statusUpdate': status,
            'oneTareaSubordinada': OneTareaSubordinada,
        }

        # Return Section
        return render(request, 'Tarea_Subordinada/updateTareaSubordinada.html', {'data':context})

    else:
        return redirect('login')




# Métodos Complementarios
# --------------------------------------------
# CRUD: Tarea Subordinada

# METHOD: POST
def AddTareaSubordinada(request, nombre, descripcion, prioridadFk, estadoFk, tareaFk):
    if authenticated:
        token = request.COOKIES.get('validate')
        headers = {'Accept-Encoding': 'UTF-8', 'Content-Type': 'application/json', 'Authorization': 'Bearer '+token, 'Accept': '*/*' }

        # Datos a enviar a la petición POST
        payload = json.dumps({'nombreSubordinada' : nombre,
                              'descripcionSubordinada': descripcion,
                              'fkPrioridadTarea': int(prioridadFk),
                              'fkEstadoTarea': int(estadoFk),
                              'fkIdTarea': int(tareaFk),
        })
        r = requests.post('http://localhost:32482/api/TareaSubordinada/add', headers=headers, data=payload)

# METHOD: PUT
def EditTareaSubordinada(request, nombre, descripcion, prioridadFk, estadoFk, tareaFk, idTareaSubordinadaToSearch):
    if authenticated:
        token = request.COOKIES.get('validate')
        headers = {'Accept-Encoding': 'UTF-8', 'Content-Type': 'application/json', 'Authorization': 'Bearer '+ token,'Accept': '*/*' }


        # Datos a enviar a la petición PUT
        payload = json.dumps({'nombreSubordinada' : nombre,
                              'descripcionSubordinada': descripcion,
                              'fkPrioridadTarea': int(prioridadFk),
                              'fkEstadoTarea': int(estadoFk),
                              'fkIdTarea': int(tareaFk),
        })
        r = requests.put('http://localhost:32482/api/TareaSubordinada/update/' + str(idTareaSubordinadaToSearch), headers=headers, data=payload)
        