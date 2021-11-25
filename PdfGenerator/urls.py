from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from PdfGenerator.views import TestPDF, GrafictSection

urlpatterns = [
    path('pdf/1',TestPDF.as_view(), name='pdf_generator'),
    path('pdf/2',GrafictSection, name='pdf_generator2'),
]
