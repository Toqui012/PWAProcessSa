from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from PdfGenerator.views import TestPDF, GrafictSection

from PdfGenerator.views import PDFSection, ReporteEmpleados, ReporteTareaSubordinada, TestPDF

urlpatterns = [
    path('pdf/',GrafictSection, name='pdf_generator'),
]
