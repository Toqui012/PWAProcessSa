from json import dump
from django.http.request import HttpRequest
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.context_processors import request
from requests.api import head
from LoginApp.views import authenticated, decodered
import requests, jwt, json

# Create your views here.

def AsignarTareaSection(request):
    if authenticated:

        

        print("Hello world :D")
        return render(request, 'Asignar_Tarea/asignar_tarea.html')
    else: 
        redirect('login')
