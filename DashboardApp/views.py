from json import dump
# from django.http.request import HttpRequest
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.context_processors import request
from LoginApp.views import authenticated, decodered
import requests, jwt, json

# Create your views here.

def DashboardMain(request):
    if authenticated(request):

        #Variables con data a enviar a la vista
        context = {
        }

        # Return Section
        return render(request, 'dashboard.html', {'data': context})
    else:
        return redirect('login')

def UserSection(request):
    if authenticated(request):
        # Consumo de API: Usuario
        # Method: GET
        token = request.COOKIES.get('validate')
        headers = {'Content-Type':'application/json', 'Authorization': 'Bearer '+ token}
        req = requests.get('http://localhost:32482/api/usuario', headers=headers)
        dataAPI = req.json()
        listUser = dataAPI['data']

        #Variables con data a enviar a la vista
        context = {
            'users': listUser
        }
        # Return Section
        return render(request, 'list_user.html', {'data': context})
    else:
        return redirect('login')

def AddUserSection(request):
    if authenticated(request):
        # Consumo de API: Rol
        # Method: GET
        token = request.COOKIES.get('validate')
        headers = {'Content-Type':'application/json', 'Authorization': 'Bearer '+ token}
        resRole = requests.get('http://localhost:32482/api/rol', headers=headers)
        dataRole = resRole.json()
        listRole = dataRole['data']

        #Consumo de API: Unidad Interna
        # Method: GET
        resUnidad = requests.get('http://localhost:32482/api/unidadInterna', headers=headers)
        dataUnidad = resUnidad.json()
        listUnidad = dataUnidad['data']

        #Consumo de API: Usuario
        # Method: POST
        rut = request.POST.get('rutUsuario')
        firstName = request.POST.get('primerNombre')
        secondName = request.POST.get('segundoNombre')
        lastName = request.POST.get('apellidoUsuario')
        secondLastName = request.POST.get('segundoApellido')
        email = request.POST.get('correoElectronico')
        numberPhone = request.POST.get('numTelefono')
        roleUser = request.POST.get('selectRolUsuario')
        internalDrive = request.POST.get('selectUnidadInterna')
        password = request.POST.get('password')

        #Configuración de los parametros para ejecutar la petición
        headers = {'Accept-Encoding': 'UTF-8', 'Content-Type': 'application/json', 'Authorization': 'Bearer '+ token,'Accept': '*/*' }

        # Datos a enviar a la petición POST
        payload = json.dumps({'rutUsuario': rut, 
                              'nombreUsuario': firstName, 
                              'segundoNombre': secondName,
                              'apellidoUsuario': lastName,
                              'segundoApellido': secondLastName,
                              'numTelefono': int(numberPhone),
                              'correoElectronico': email,
                              'password': password,
                              'idRolUsuario': int(roleUser),
                              'idUnidadInternaUsuario': int(internalDrive),
        })

        # Section: Validate API
        status = False
        r = requests.post('http://localhost:32482/api/usuario/add', headers=headers, data=payload)
        if r.ok:
            status = True

        # Variables con data a enviar a la vista
        context = {
            'role': listRole,
            'unidadInterna': listUnidad
        }
        #Return Section
        return render(request, 'user.html',{'data':context})
    else:
        return redirect('login')


