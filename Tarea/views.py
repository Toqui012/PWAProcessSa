from django.shortcuts import render
from json import dump
from django.http.request import HttpRequest
# from django.http.request import HttpRequest
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.context_processors import request
from LoginApp.views import authenticated, decodered
import requests, jwt, json

# Create your views here.


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
        return render(request, 'list_tarea.html', {'data': context})
    else:
        return redirect('login')


def AddTareaSection(request):
    if authenticated(request):
        # Consumo de API: Usuario
        # Method: GET
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
        problem_report = request.POST.get('problemasReportados')
        assignment = request.POST.get('asignacion')
        responsible = request.POST.get('selectrutUsuario')
        justification = request.POST.get('selectJustificacion')
        taskState = request.POST.get('selectEstadoTarea')
        taskPriority = request.POST.get('selectPrioridad')
        print(nombreTarea,description,dateDeadline,problem_report,assignment,responsible,justification,taskState,taskPriority)
        
        # Optimizar más con try catch
        status = ''
        if nombreTarea == '' or description == '' or dateDeadline == '' or problem_report == '' or assignment == '' or responsible == '' or taskState == '' or taskPriority == '' or nombreTarea == None:
            status = 'ERROR'
        elif nombreTarea != '' or description != '' or dateDeadline != '' or problem_report != '' or assignment != '' or responsible != '' or taskState != '' or taskPriority != '' or nombreTarea != None:
            status = 'OK'
        else:
            status
        if  status == 'OK':
            AddTarea(request,nombreTarea,description,dateDeadline,problem_report,assignment,responsible,justification,taskState,taskPriority)

        # Variables con data a enviar a la vista
        context = {
            'user': listUser,
            'prioridad': listPrioridad,
            'estado': listEstado,
            'justificacion': listJustificacion
        }
        #Return Section
        return render(request, 'add_tarea.html',{'data':context})
    else:
        return redirect('login')


def AddTarea(request,nombreTarea,description,dateDeadline,problem_report,assignment,responsible,justification,taskState,taskPriority):
    if authenticated:
        token = request.COOKIES.get('validate')
        headers = {'Accept-Encoding': 'UTF-8', 'Content-Type': 'application/json', 'Authorization': 'Bearer '+ token,'Accept': '*/*' }


        # Datos a enviar a la petición POST
        payload = json.dumps({
                                'nombreTarea':nombreTarea,
                                'descripcionTarea': description,
                                'fechaPlazo': dateDeadline,
                                'reporteProblema': problem_report,
                                'asignacionTarea': assignment,
                                'fkRutUsuario' : responsible,
                                'fkIdJustificacion': int(justification),
                                'fkEstadoTarea' : int(taskState),
                                'fkPrioridadTarea' : int(taskPriority),
        })
        r = requests.post('http://localhost:32482/api/tarea/add', headers=headers, data=payload)

    
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
            return render(request, 'list_tarea.html', {'data':context})

    else:
        return redirect('login')
