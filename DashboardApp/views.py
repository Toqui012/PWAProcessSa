from django.http.request import HttpHeaders
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.context_processors import request
from LoginApp.views import authenticated, decodered

# Create your views here.

def DashboardMain(request):
    if authenticated(request):
        token = request.COOKIES.get('validate')
        data = decodered(token)
        context = {
                'menu' : 'DashboardMain',
                'email' : data['email'],
                'name': data['unique_name'],
                'login' : datetime.fromtimestamp(data['nbf'])
        }
        return render(request, 'dashboard.html',{'datos': context})
    