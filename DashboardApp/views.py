from django.http.request import HttpHeaders
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.context_processors import request
from LoginApp.views import authenticated, decodered

# Create your views here.

def DashboardMain(request):
    if authenticated(request):
        return render(request, 'dashboard.html')
    else:
        return redirect('login')
