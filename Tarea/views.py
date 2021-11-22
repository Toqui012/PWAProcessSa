from django.shortcuts import render
from json import dump
from django.http.request import HttpRequest
# from django.http.request import HttpRequest
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.context_processors import request
from LoginApp.views import authenticated, decodered
import requests, jwt, json
from datetime import date


# Create your views here.

def AddTareaSection(request):
    if authenticated(request):

        token = request.COOKIES.get('validate')
        headers = {'Content-Type':'application/json', 'Authorization': 'Bearer '+ token}
        
        #consumo de api : usuarios
        # Method: GET
        resUser = requests.get('http://localhost:32482/api/usuario', headers=headers)
        dataUser = resUser.json()
        listUser = dataUser['data']

        #consumo de api : prioridad tarea
        # Method: GET
        resPrioridad = requests.get('http://localhost:32482/api/prioridadTarea', headers=headers)
        dataPrioridad = resPrioridad.json()
        listPrioridad = dataPrioridad['data']

        #consumo api: estado tarea
        # Method: GET
        resEstado = requests.get('http://localhost:32482/api/estadoTarea', headers=headers)
        dataEstado = resEstado.json()
        listEstado = dataEstado['data']
        
        #consumo api: Justificacion
        # Method: GET
        resJustificacion = requests.get('http://localhost:32482/api/justificacionTarea', headers=headers)
        dataJustificacion = resJustificacion.json()
        listJustificacion = dataJustificacion['data']

        #consumo de API: Tarea
        # Method: POST
        nombreTarea = request.POST.get('nameTarea')
        description = request.POST.get('descripcion')
        dateDeadline = request.POST.get('fechaPlazo')
        taskPriority = request.POST.get('selectPrioridad')
        #print(nombreTarea,description,dateDeadline,problem_report,assignment,responsible,justification,taskState,taskPriority)
        
        # Optimizar más con try catch
        status = ''
        if nombreTarea == '' or description == '' or dateDeadline == '' or taskPriority == '' or nombreTarea == None:
            status = 'ERROR'
        elif nombreTarea != '' or description != '' or dateDeadline != '' or taskPriority != '' or nombreTarea != None:
            status = 'OK'
        else:
            status
        if  status == 'OK':
            AddTarea(request,nombreTarea,description,dateDeadline,taskPriority)

        print(status)

        # Variables con data a enviar a la vista
        context = {
            'user': listUser,
            'prioridad': listPrioridad,
            'estado': listEstado,
            'justificacion': listJustificacion
        }
        #Return Section
        return render(request, 'Tareas/add_tarea.html',{'data':context})
    else:
        return redirect('login')


def TareaSection(request):
    if authenticated(request):
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
        return render(request, 'Tareas/list_tarea.html', {'data': context})
    else:
        return redirect('login')


def EditUserSection(request, idTarea):
    if authenticated(request):
        status = 'NO_CONTENT'
        token = request.COOKIES.get('validate')
        headers = {'Accept-Encoding': 'UTF-8', 'Content-Type': 'application/json', 'Authorization': 'Bearer '+ token,'Accept': '*/*' }


        #consumo de api : usuarios
        # Method: GET
        resUser = requests.get('http://localhost:32482/api/usuario', headers=headers)
        dataUser = resUser.json()
        listUser = dataUser['data']

        #consumo de api : prioridad tarea
        # Method: GET
        resPrioridad = requests.get('http://localhost:32482/api/prioridadTarea', headers=headers)
        dataPrioridad = resPrioridad.json()
        listPrioridad = dataPrioridad['data']

        #consumo api: estado tarea
        # Method: GET
        resEstado = requests.get('http://localhost:32482/api/estadoTarea', headers=headers)
        dataEstado = resEstado.json()
        listEstado = dataEstado['data']
        
        #consumo api: Justificacion
        # Method: GET
        resJustificacion = requests.get('http://localhost:32482/api/justificacionTarea', headers=headers)
        dataJustificacion = resJustificacion.json()
        listJustificacion = dataJustificacion['data']

        #consumo de API: OneTarea
        # method: get with params
        idTareaP=str(idTarea)
        resOneTarea = requests.get('http://localhost:32482/api/tarea/oneTask/'+ idTareaP, headers=headers)
        dataOneTarea = resOneTarea.json()
        OneTarea = dataOneTarea['data']

        # ASignacion del rut a buscar
        tareaToSearch = ''
        for x in OneTarea:
            tareaToSearch = x['idTarea']

        # validate data Extraction
        if request.method == 'POST':
            try:
                nombreTarea = request.POST.get('nameTarea')
                description = request.POST.get('descripcion')
                dateDeadline = request.POST.get('fechaPlazo')
                responsible = request.POST.get('selectrutUsuario')
                taskState = request.POST.get('selectEstadoTarea')
                taskPriority = request.POST.get('selectPrioridad')
                status = 'OK'

                print(dateDeadline)
                    
            except:
                status = 'ERROR'
        
        
            print(status)
        # metodo update User
            try:
             if status == 'OK':
              EditTarea(request,nombreTarea,description,dateDeadline,responsible,taskState,taskPriority,tareaToSearch)
            except:
                status = 'ERROR'
        #print(nombreTarea,description,dateDeadline,problem_report,assignment,responsible,justification,taskState,taskPriority)    
        context = {
            'usuario':listUser,
            'prioridad':listPrioridad,
            'estado':listEstado,
            'justificacion':listJustificacion,
            'oneTarea': OneTarea,
        }

        # return Section
        return render(request, 'Tareas/tarea_edit.html', {'data':context})
    else:
        return redirect('login')

    
def DeleteTareaSection(request, idTarea):
    if authenticated:
        status = 'NO_CONTENT'
        token = request.COOKIES.get('validate')
        headers = {'Accept-Encoding': 'UTF-8', 'Content-Type': 'application/json', 'Authorization': 'Bearer '+ token,'Accept': '*/*' }


        payload = json.dumps({'idTarea': idTarea})
        r = requests.delete('http://localhost:32482/api/tarea/delete/'+idTarea, headers=headers, data=payload)

        reqTarea = requests.get('http://localhost:32482/api/tarea', headers=headers)
        dataAPI = reqTarea.json()
        listTarea = dataAPI['data']

        context = {
            'tareas' : listTarea,
            'deleteStatus' : status,
        }

        if r.ok:
            status = 'DELETED'
            print(status)
            return redirect('TareaSection')
        else:
            status = 'ERROR'
            print(status)
            return render(request, 'Tareas/list_tarea.html', {'data':context})

    else:
        return redirect('login')

def AddTarea(request,nombreTarea,description,dateDeadline,taskPriority):
    if authenticated:
        token = request.COOKIES.get('validate')
        headers = {'Accept-Encoding': 'UTF-8', 'Content-Type': 'application/json', 'Authorization': 'Bearer '+ token,'Accept': '*/*' }


        # Datos a enviar a la petición POST
        payload = json.dumps({
                                'nombreTarea':nombreTarea,
                                'descripcionTarea': description,
                                'fechaPlazo': dateDeadline,
                                'fkRutUsuario' : '0.000.000',
                                'porcentajeAvance': 5,
                                'fechaCreacion': dateDeadline,
                                'creadaPor': '0.000.000',
                                'fkEstadoTarea' : 1,
                                'fkPrioridadTarea' : int(taskPriority),
        })

        r = requests.post('http://localhost:32482/api/tarea/add', headers=headers, data=payload)

def EditTarea(request,nombreTarea,description,dateDeadline,responsible,taskState,taskPriority,tareaToSearch):

    if authenticated:
        token = request.COOKIES.get('validate')
        headers = {'Accept-Encoding': 'UTF-8', 'Content-Type': 'application/json', 'Authorization': 'Bearer '+ token,'Accept': '*/*' }

        
        payload = json.dumps({
                                'idTarea':tareaToSearch,
                                'nombreTarea':nombreTarea,
                                'descripcionTarea': description,
                                'fechaPlazo': dateDeadline,
                                'fkRutUsuario' : '0.000.000',
                                'porcentajeAvance': 5,
                                'fechaCreacion': dateDeadline,
                                'creadoPor': '0.000.000',
                                'fkEstadoTarea' : int(taskState),
                                'fkPrioridadTarea' : int(taskPriority),
        })
        tareaP=str(tareaToSearch)
        r = requests.put('http://localhost:32482/api/tarea/update/'+tareaP, headers=headers, data=payload)
        print(r)




    