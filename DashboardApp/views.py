from json import dump
from django.http.request import HttpRequest
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
        
        # Optimizar más con try catch
        status = ''
        if rut == '' or firstName == '' or secondName == '' or lastName == '' or secondLastName == '' or email == '' or numberPhone == '' or numberPhone == None or roleUser == '' or internalDrive == '' or password == '':
            status = 'ERROR'
        elif rut != '' or firstName != '' or secondName != '' or lastName != '' or secondLastName != '' or email != '' or numberPhone != '' or roleUser != '' or internalDrive != '' or password != '':
            status = 'OK'
        else:
            status

        if  status == 'OK':
            AddUser(request,rut,firstName,secondName,lastName,secondLastName,email,numberPhone,roleUser,internalDrive,password)

        # Variables con data a enviar a la vista
        context = {
            'role': listRole,
            'unidadInterna': listUnidad,
            'statusCreation': status,
        }
        #Return Section
        return render(request, 'user.html',{'data':context})
    else:
        return redirect('login')

def DeleteUserSection(request, idUser):
    if authenticated:
        status = 'NO_CONTENT'
        token = request.COOKIES.get('validate')
        headers = {'Accept-Encoding': 'UTF-8', 'Content-Type': 'application/json', 'Authorization': 'Bearer '+ token,'Accept': '*/*' }
        
        # Consumo de API: Usuario
        # Method: DELETE
        payload = json.dumps({'rutUsuario': idUser})
        r = requests.delete('http://localhost:32482/api/usuario/delete/'+idUser, headers=headers, data=payload)

        # Consumo de API: Usuario
        # Method: GET
        reqUser = requests.get('http://localhost:32482/api/usuario', headers=headers)
        dataAPI = reqUser.json()
        listUser = dataAPI['data']

        context = {
            'users': listUser,
            'deteleStatus':status,
        }

        if r.ok:
            status = 'DELETED'
            print(status)
            return redirect('UserSection')
        else:
            status = 'ERROR'
            print(status)
            return render(request, 'list_user.html', {'data':context})
    else:
        return redirect('login')

def EditUserSection(request, idUser):
    if authenticated:

        # Configuración Header
        status = 'NO_CONTENT'
        token = request.COOKIES.get('validate')
        headers = {'Accept-Encoding': 'UTF-8', 'Content-Type': 'application/json', 'Authorization': 'Bearer '+ token,'Accept': '*/*' }

        # Consumo de API: Rol
        # Method: GET
        resRole = requests.get('http://localhost:32482/api/rol', headers=headers)
        dataRole = resRole.json()
        listRole = dataRole['data']


        # Consumo de API: Unidad Interna
        # Method: GET
        resUnidad = requests.get('http://localhost:32482/api/unidadInterna', headers=headers)
        dataUnidad = resUnidad.json()
        listUnidad = dataUnidad['data']

        # Consumo de API: OneUser
        # Method: GET with Params
        resOneUser = requests.get('http://localhost:32482/api/usuario/oneUser/'+ idUser, headers=headers)
        dataOneUser = resOneUser.json()
        OneUser = dataOneUser['data']

        # Fillings in Fields
        # for x in OneUser:
            

        # Validate Data Extraction
        # if request.method == 'POST':
        #     try:
        #         # Recuperación de data proveniente del HTML
        #         rut = request.POST.get('rutUsuario')
        #         firstName = request.POST.get('primerNombre')
        #         secondName = request.POST.get('segundoNombre')
        #         lastName = request.POST.get('apellidoUsuario')
        #         secondLastName = request.POST.get('segundoApellido')
        #         email = request.POST.get('correoElectronico')
        #         numberPhone = request.POST.get('numTelefono')
        #         roleUser = request.POST.get('selectRolUsuario')
        #         internalDrive = request.POST.get('selectUnidadInterna')
        #         password = request.POST.get('password')
        #         status = 'OK'
        #     except:
        #         status = 'ERROR'

        # Metodo Update User
        # try:
        #     if status == 'OK':
        #      EditUser(request,rut,firstName,secondName,lastName,secondLastName,email,numberPhone,roleUser,internalDrive,password)
        # except:
        #     status = 'ERROR'
        
        context = {
            'role': listRole,
            'unidadInterna': listUnidad,
            'statusUpdate': status,
            'oneUser': OneUser,
        }

        # Return Section
        return render(request, 'user_edit.html', {'data':context})
    else:
        return redirect('login')


# Metodos Complementarios
#-------------------------------------------
# Crud: User

# METHOD: POST
def AddUser(request,rut, firstName, secondName, lastName, secondLastName, email, numberPhone, roleUser, internalDrive, password):
    if authenticated:
        token = request.COOKIES.get('validate')
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
        r = requests.post('http://localhost:32482/api/usuario/add', headers=headers, data=payload)

def EditUser(request,rut, firstName, secondName, lastName, secondLastName, email, numberPhone, roleUser, internalDrive, password):
    if authenticated:
        token = request.COOKIES.get('validate')
        headers = {'Accept-Encoding': 'UTF-8', 'Content-Type': 'application/json', 'Authorization': 'Bearer '+ token,'Accept': '*/*' }


        # Datos a enviar a la petición PUT
        payload = json.dumps({
            'rutUsuario': rut,
            'nombreUsuario': firstName,
            'segundoNombre': secondName,
            'apellidoUsuario': lastName,
            'segundoApellido': secondLastName,
            'numTelefono': int(numberPhone),
            'correoElectronico': email,
            'password': password,
            'idRolUsuario': int(roleUser),
            'idUnidadInternaUsuario': int(internalDrive)
        })
        r = requests.put('http://localhost:32482/api/usuario/update'+rut, headers=headers, data=payload)





        








