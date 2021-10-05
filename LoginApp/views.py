from django.http import response
from typing import Any
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
import requests, jwt, json

# Función para desencriptar el token => Para obtener los valores
def decodered(data):
    data_token = jwt.decode(data,SECRET, algorithms=["H256"])
    return data_token

#Función está autenticado
def authenticated(request):
    #validate corresponde a la cookie
    if request.COOKIES.get('validate'):
        return True
    else: 
        return False

#Crea la cookie
def setCookie(tokenApi):
    obj = redirect('DashboardMain')
    # Aquí abajo está creando la cookie => Le asigna el nombre validate
    obj.set_cookie('validate', tokenApi, expires=43200)
    return obj

# Función valida datos => Se pasa al web service para que los valide
def validate(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    payload = json.dumps({'email': email, 'password': password})
    headers = {'Accept-Encoding': 'UTF-8', 'Content-Type': 'application/json', 'Accept': '*/*', 'email': email, 'password': password}
    r = requests.post('https://localhost:32482/api/login/addlogin/', headers=headers, data=payload)
    if r.ok:
        tokenAPI = r.json()
        # Generando una cookie con la respuesta que entrega el web service => r en este caso, la respuesta de ese post lo asigna a la variable tokenAPI
        obj = setCookie(tokenAPI['data']['token'])

        return obj
    else: 
        return redirect('login')

# Función login
def login(request):
    return render(request, 'login.html')

def logout(request):
    if authenticated(request):
        token = request.COOKIES.get('validate')
        rep = redirect('DashboardMain')
        rep.delete_cookie('validate') #elimina el valor de la cookie
        return rep
    else: 
        return redirect('DashboardMain')



