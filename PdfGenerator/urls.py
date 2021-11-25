from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from PdfGenerator.views import TestPDF, GrafictSection

from PdfGenerator.views import PDFSection, ReporteEmpleados, ReporteEmpresas, ReporteTareaSubordinada, TestPDF

urlpatterns = [
    path('pdfSection/', PDFSection, name='PDFSection'),
    # PDF Tarea
    path('pdfTarea/',TestPDF.as_view(), name='pdf_generator'),
    # PDF Tarea Subordinada
    #path('pdfTareaSubordinada/', ReporteTareaSubordinada.as_view(), name='ReporteTareaSubordinada'),
    # PDF Empresas
    #path('pdfEmpresa/', ReporteEmpresas.as_view(), name='ReporteEmpresa'),
    # PDF Empleados
    #path('pdfEmpleado/', ReporteEmpleados.as_view(), name='ReporteEmpleado'),

    path('pdf/1',TestPDF.as_view(), name='pdf_generator'),
    path('pdf/2',GrafictSection, name='pdf_generator2'),
]
