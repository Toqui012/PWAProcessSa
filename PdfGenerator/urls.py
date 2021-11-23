from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from PdfGenerator.views import TestPDF

urlpatterns = [
    path('pdf/',TestPDF.as_view(), name='pdf_generator'),
]
