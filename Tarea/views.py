from django.shortcuts import render

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

        #consumo de API: Tarea
        # Method: POST
        nombreTarea = request.POST.get('nameTarea')
        description = request.POST.get('descripcion')
        dateDeadline = request.POST.get('fechaPlazo')
        problem_report = request.POST.get('problemasReportados')
        assignment = request.POST.get('asignacion')
        responsible = request.POST.get('rutUsuario')
        justification = request.POST.get('justificacion')
        taskState = request.POST.get('estadoTarea')
        taskPriority = request.POST.get('prioridadTarea')

        #Configuración de los parametros para ejecutar la petición
        headers = {'Accept-Encoding': 'UTF-8', 'Content-Type': 'application/json', 'Authorization': 'Bearer '+ token,'Accept': '*/*' }

        # Datos a enviar a la petición POST
        payload = json.dumps({
                                'nameTarea':nombreTarea,
                                'descripcion': description,
                                'fechaPlazo': dateDeadline,
                                'problemasReportados': problem_report,
                                'asignacion': assignment,
                                'rutUsuario' : responsible,
                                'justificacion': justification,
                                'estadoTarea' : taskState,
                                'prioridadTarea' : taskPriority,
        })

        # Section: Validate API
        status = False
        r = requests.post('http://localhost:32482/api/tarea/add', headers=headers, data=payload)
        if r.ok:
            status = True

        # Variables con data a enviar a la vista
        context = {
            'user': listUser,
            'prioridad': listPrioridad,
            'estado': listEstado
        }
        #Return Section
        return render(request, 'add_tarea.html',{'data':context})
    else:
        return redirect('login')



