from django.http.request import HttpHeaders
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.context_processors import request

def LoginView(request): 
    return render(request, 'login.html',{})
# Create your views here.

