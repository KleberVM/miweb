from django.urls import path
from . import views

app_name = 'encuesta'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('crear/', views.EncuestaCreateView.as_view(), name='crear'),
    path('exito/', views.EncuestaSuccessView.as_view(), name='success'),
    path('excel/', views.ExcelExportView.as_view(), name='excel_export'),
    path('excel/download/', views.DownloadExcelView.as_view(), name='download_excel'),
    path('subir/', views.ExcelUploadView.as_view(), name='excel_upload'),
    path('subir/procesar/', views.ProcessExcelUploadView.as_view(), name='process_excel_upload'),
]