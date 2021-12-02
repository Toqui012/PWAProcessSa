from json import dump
from django.http.request import HttpRequest
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.context_processors import request
from requests.api import head
from LoginApp.views import authenticated, decodered
import requests, jwt, json

def EmpresaSection(request):
    if(authenticated):
        token = request.COOKIES.get('validatepwa')
        test = decodered(token)
        headers = {'Content-Type':'application/json', 'Authorization': 'Bearer '+ token}
        req = requests.get('http://localhost:32482/api/business', headers=headers)
        dataAPI = req.json()
        listEmpresa = dataAPI['data']

        # Variables a enviar a la vista
        context = {
            'empresa': listEmpresa,
            'rutUsuarioLogeado': test['nameid']
        }

        return render(request, 'Empresas/list_empresa.html', {'data': context})

def AddEmpresaSection(request):
    if authenticated(request):
        # Consumo de API: Empresa
        token = request.COOKIES.get('validatepwa')
        test = decodered(token)
        headers = {'Content-Type':'application/json', 'Authorization': 'Bearer '+ token}
        resEmpresa = requests.get('http://localhost:32482/api/business', headers=headers)
        dataEmpresa = resEmpresa.json()
        listEmpresa = dataEmpresa['data']

        rut = request.POST.get('rutEmpresa')
        razonSocial = request.POST.get('razonSocialEmpresa')
        giro = request.POST.get('giroEmpresa')
        direccion = request.POST.get('direccionEmpresa')
        numeroTelefono = request.POST.get('numeroTelefonoEmpresa')
        correoElectronico = request.POST.get('correoElectronicoEmpresa')

        status = ''
        if rut == '' or razonSocial == '' or giro == '' or direccion == '' or numeroTelefono == '' or correoElectronico == '' or razonSocial == None:
            status = 'ERROR'
        elif rut != '' or razonSocial != '' or giro != '' or direccion != '' or numeroTelefono != '' or correoElectronico != '' or razonSocial != None:
            status = 'OK'
        else: 
            status
        
        if status == 'OK':
            AddEmpresa(request, rut, razonSocial, giro, direccion, numeroTelefono, correoElectronico)

        print(status)

        # Variables con data para enviar a la vista
        context = {
            'empresa': listEmpresa,
            'statusCreation': status,
            'rutUsuarioLogeado': test['nameid']

        }

        # Return Section
        return render(request, 'Empresas/add_empresa.html', {'data': context})
    
    else:
        return redirect('login')

def DeleteEmpresaSection(request, rutEmpresa):
    if authenticated:
        status = 'NO_CONTENT'
        token = request.COOKIES.get('validatepwa')
        test = decodered(token)
        headers = {'Accept-Encoding': 'UTF-8', 'Content-Type': 'application/json', 'Authorization': 'Bearer '+ token,'Accept': '*/*' }

        # Consumo de API: Empresa
        # METHOD: DELETE
        payload = json.dumps({'rutEmpresa': rutEmpresa})
        r = requests.delete('http://localhost:32482/api/business/delete/' + rutEmpresa, headers=headers, data=payload)

        # Consumo API: Empresa
        reqEmpresa = requests.get('http://localhost:32482/api/business', headers=headers)
        dataAPI = reqEmpresa.json()
        listEmpresa = dataAPI['data']

        context = {
            'empresa': listEmpresa, 
            'deleteStatus': status,
            'rutUsuarioLogeado': test['nameid']
        }

        if r.ok:
            status = 'DELETED'
            print(status)
            return redirect('EmpresaSection')
        else:
            status = 'ERROR'
            print(status)
            return render(request, 'Empresas/list_empresa.html', {'data': context})
    
    else:
        return redirect('login')


def EditEmpresaSection(request, rutEmpresa):
    if authenticated:

        # Configuración Header
        status = 'NO_CONTENT'
        token = request.COOKIES.get('validatepwa')
        test = decodered(token)
        headers = {'Accept-Encoding': 'UTF-8', 'Content-Type': 'application/json', 'Authorization': 'Bearer '+ token,'Accept': '*/*' }       

        # Consumo de API: OneEmpresa
        # METHOD: GET WITH PARAMS
        resOneEmpresa = requests.get('http://localhost:32482/api/business/oneBusiness/' + rutEmpresa, headers=headers)
        dataOneEmpresa = resOneEmpresa.json()
        OneEmpresa = dataOneEmpresa['data']

        # Asignación del rut a buscar
        rutEmpresaToSearch = ''
        for x in OneEmpresa:
            rutEmpresaToSearch = x['rutEmpresa']
        
        # Validate Data Extraction
        if request.method == 'POST':
            # Recuperación de data proveniente del HTML
            rut = request.POST.get('rutEmpresa')
            razonSocial = request.POST.get('razonSocialEmpresa')
            giro = request.POST.get('giroEmpresa')
            direccion = request.POST.get('direccionEmpresa')
            numeroTelefono = request.POST.get('numeroTelefonoEmpresa')
            correoElectronico =request.POST.get('correoElectronicoEmpresa')
            status = 'OK'

        # Método Update Empresa
        try:
            if status == 'OK':
                EditEmpresa(request, rut, razonSocial, giro, direccion, numeroTelefono, correoElectronico, rutEmpresaToSearch)

        except:
            status = 'ERROR'

        context = {
            'statusUpdate': status,
            'oneEmpresa': OneEmpresa,
            'rutUsuarioLogeado': test['nameid']
        }

        # Return Section
        return render(request, 'Empresas/edit_empresa.html', {'data': context})
    
    else:
        return redirect('login')

# Métodos Complementarios
# -----------------------------------------
# CRUD: Empresa

# METHOD: POST
def AddEmpresa(request, rut, razonSocial, giro, direccion, numeroTelefono, correoElectronico):
    if authenticated:
        token = request.COOKIES.get('validatepwa')
        headers = {'Accept-Encoding': 'UTF-8', 'Content-Type': 'application/json', 'Authorization': 'Bearer '+token, 'Accept': '*/*' }        

        # Datos a enviar a la petición PUT
        payload = json.dumps({'rutEmpresa': rut,
                              'razonSocial': razonSocial,
                              'giroEmpresa': giro,
                              'direccionEmpresa': direccion,
                              'numeroTelefono': int(numeroTelefono),
                              'correoElectronicoEmpresa': correoElectronico,
                            })

        r = requests.post('http://localhost:32482/api/business/add', headers=headers, data=payload)

        print (r)

def EditEmpresa(request, rut, razonSocial, giro, direccion, numeroTelefono, correoElectronico, rutEmpresaToSearch):
    if authenticated:
        token = request.COOKIES.get('validatepwa')
        headers = {'Accept-Encoding': 'UTF-8', 'Content-Type': 'application/json', 'Authorization': 'Bearer '+token, 'Accept': '*/*' }        

        # Datos a enviar a la petición PUT
        payload = json.dumps({'rutEmpresa': rut,
                              'razonSocial': razonSocial,
                              'giroEmpresa': giro,
                              'direccionEmpresa': direccion,
                              'numeroTelefono': int(numeroTelefono),
                              'correoElectronicoEmpresa': correoElectronico
                            })

        r = requests.put('http://localhost:32482/api/business/update/' + rutEmpresaToSearch, headers=headers, data=payload)
