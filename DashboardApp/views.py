from django.http.request import HttpHeaders
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.context_processors import request

# Create your views here.

def DashboardMain(request):
    return render(request, 'dashboard.html',{})