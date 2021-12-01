from json import dump
from django.http.request import HttpRequest
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.context_processors import request
from requests.api import head
from LoginApp.views import authenticated, decodered
import requests, jwt, json

def UnidadInternaSection(request):
    if(authenticated): 
        token = request.COOKIES.get('validate')
        headers = {'Content-Type':'application/json', 'Authorization': 'Bearer '+ token}
        req = requests.get('http://localhost:32482/api/unidadInterna', headers=headers)
        dataAPI = req.json()
        listUnidadInterna = dataAPI['data']

        reqUser = requests.get('http://localhost:32482/api/usuario', headers=headers)
        dataAPIUser = reqUser.json()
        listUser = dataAPIUser['data']

        test = decodered(token)
        print(test['nameid'])

        # Código Filtrado
        filtroUnidadInterna = None

        filtroEmpresa = None

        for i in listUser:
            if test['nameid'] == i['rutUsuario']:
                filtroUnidadInterna = i['idUnidadInternaUsuario']

        for i in listUnidadInterna:
            if filtroUnidadInterna == i['idUnidadInterna']:
                filtroEmpresa = i['fkRutEmpresa']

        reqFiltroUnidadInterna = requests.get('http://localhost:32482/api/unidadInterna/getUnidadInternaByBusiness/' + str(filtroEmpresa), headers=headers)
        dataAPIFiltrado = reqFiltroUnidadInterna.json()
        listaFiltrada = dataAPIFiltrado['data']
        print(listaFiltrada)


        # Variables a enviar a la vista
        context = {
            'unidadInterna': listaFiltrada
        }

        return render(request, 'Unidad_Interna/list_unidad_interna.html', {'data': context})

def AddUnidadInternaSection(request):
    if authenticated(request):
        # Consumo de API: Empresa
        # Method: GET
        token = request.COOKIES.get('validate')
        headers = {'Content-Type':'application/json', 'Authorization': 'Bearer '+ token}
        resEmpresa = requests.get('http://localhost:32482/api/business', headers=headers)
        dataEmpresa = resEmpresa.json()
        listEmpresa = dataEmpresa['data']

        # Consumo de API: Unidad Interna
        nombre = request.POST.get('nombreUnidadInterna')
        descripcion = request.POST.get('descripcionUnidadInterna')
        fkRutEmpresa = request.POST.get('fkRutEmpresa')

        status = ''

        if nombre == '' or descripcion == '' or fkRutEmpresa == '' or nombre == None:
            status = 'ERROR'
        elif nombre != '' or descripcion != '' or fkRutEmpresa != '' or nombre != None:
            status = 'OK'
        else:
            status

        if status == 'OK':
            AddUnidadInterna(request, nombre, descripcion, fkRutEmpresa)

        # Variables con data a enviar a la vista
        context = {
            'empresa': listEmpresa,
            'statusCreation': status,
        }

        # Return Section
        return render(request, 'Unidad_Interna/add_unidad_interna.html', {'data': context})

def DeleteUnidadInternaSection(request, idUnidadInterna): 
    if authenticated:
        status = 'NO_CONTENT'
        token = request.COOKIES.get('validate')
        headers = {'Content-Type':'application/json', 'Authorization': 'Bearer '+ token}

        # Consumo de API: Unidad Interna
        # METHOD: DELETE
        unidadInt = str(idUnidadInterna)
        payload = json.dumps({'idUnidadInterna': unidadInt})
        r = requests.delete('http://localhost:32482/api/unidadInterna/delete/' + unidadInt, headers=headers, data=payload)
        print(r)

        # Consumo de API: Unidad Interna
        # METHOD: GET
        reqUnidadInterna = requests.get('http://localhost:32482/api/unidadInterna', headers=headers)
        dataAPI = reqUnidadInterna.json()
        listUnidadInterna = dataAPI['data']

        context = {
            'unidadInterna': listUnidadInterna,
            'deleteStatus': status
        }

        if r.ok:
            status = 'DELETED'
            print(status)
            return redirect('UnidadInternaSection')
        else:
            status = 'ERROR'
            print(status)
            return render(request, 'Unidad_Interna/list_unidad_interna.html', {'data': context})

    else:
        return redirect('login')

def EditUnidadInternaSection(request, idUnidadInterna):
    if authenticated:
        # Configuración del header
        status = 'NO_CONTENT'
        token = request.COOKIES.get('validate')
        headers = {'Content-Type':'application/json', 'Authorization': 'Bearer '+ token}
        
        # Consumo de API: Empresa
        # METHOD: GET
        resEmpresa = requests.get('http://localhost:32482/api/business', headers=headers)
        dataEmpresa = resEmpresa.json()
        listEmpresa = dataEmpresa['data']

        # Consumo de API: OneUnidadInterna
        # METHOD: GET with Params
        unidadInt = str(idUnidadInterna)
        resOneUnidadInterna = requests.get('http://localhost:32482/api/unidadInterna/oneUnidadInterna/' + unidadInt, headers=headers)
        dataOneUnidadInterna = resOneUnidadInterna.json()
        OneUnidadInterna = dataOneUnidadInterna['data']

        # Asignación del ID de la Unidad Interna a Buscar
        idUnidadInternaToSearch = ''
        for x in OneUnidadInterna:
            idUnidadInternaToSearch = x['idUnidadInterna']

        # Validate Data Extraction
        if request.method == 'POST':
            try:
                # Recuperación de data proveniente del HTML
                nombre = request.POST.get('nombreUnidadInterna')
                descripcion = request.POST.get('descripcionUnidadInterna')
                fkRutEmpresa = request.POST.get('fkRutEmpresa')
                status = 'OK'

            except:
                status = 'ERROR'


        # Método Update Unidad Interna
        try:
            if status == 'OK':
                EditUnidadInterna(request, nombre, descripcion, fkRutEmpresa, idUnidadInternaToSearch)

        except:
            status = 'ERROR'

        context = {
            'empresa': listEmpresa,
            'statusUpdate': status,
            'oneUnidadInterna': OneUnidadInterna
        }

        # Return Section
        return render(request, 'Unidad_Interna/update_unidad_interna.html', {'data': context})

    else:
        return redirect('login')



# Métodos Complementarios
# ----------------------------------------
# CRUD: Unidad Interna

# METHOD: POST
def AddUnidadInterna(request, nombre, descripcion, fkRutEmpresa):
    if authenticated:
        token = request.COOKIES.get('validate')
        headers = {'Content-Type':'application/json', 'Authorization': 'Bearer '+ token}

        # Datos a enviar a la petición POST
        payload = json.dumps({'nombreUnidad': nombre,
                              'descripcionUnidad': descripcion,
                              'fkRutEmpresa': fkRutEmpresa,
        })

        r = requests.post('http://localhost:32482/api/unidadInterna/add', headers=headers, data=payload)

def EditUnidadInterna(request, nombre, descripcion, fkRutEmpresa, idUnidadInternaToSearch):
    if authenticated:
        token = request.COOKIES.get('validate')
        headers = {'Content-Type':'application/json', 'Authorization': 'Bearer '+ token}

        # Datos a enviar a la petición PUT
        payload = json.dumps({'nombreUnidad': nombre,
                              'descripcionUnidad': descripcion,
                              'fkRutEmpresa': fkRutEmpresa,
        })

        print(payload)

        r = requests.put('http://localhost:32482/api/unidadInterna/update/' + str(idUnidadInternaToSearch), headers=headers, data=payload)

        print(r)