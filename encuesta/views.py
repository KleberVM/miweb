from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView, View
from django.urls import reverse_lazy
from .models import Encuesta
from django import forms
import pandas as pd
import datetime
from django.http import HttpResponse
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

# Create your views here.
class HomeView(TemplateView):
    template_name = 'encuesta/home.html'

class EncuestaForm(forms.ModelForm):
    class Meta:
        model = Encuesta
        fields = '__all__'
        widgets = {
            'firmeza_voto': forms.Select(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]),
            'influencia_entorno': forms.Select(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]),
            'estabilidad': forms.Select(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]),
            'empleo': forms.Select(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]),
            'deuda': forms.Select(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]),
            'calidad': forms.Select(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]),
            'becas': forms.Select(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]),
            'corrupcion_justicia': forms.Select(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]),
            'salud': forms.Select(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]),
            'seguridad_ciudadana': forms.Select(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]),
            'cambio_climatico': forms.Select(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]),
            'temaGenero': forms.Select(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]),
            'derechos_sociales': forms.Select(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]),
            'modelo_desarrollo': forms.Select(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]),
            'PropuestaCandidatoNegativo': forms.Select(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]),
            'descontentoCandidato': forms.Select(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]),
            'emocion_dominante': forms.Select(choices=[
                ('Esperanza', 'Esperanza'),
                ('Temor', 'Temor'),
                ('Desconfianza', 'Desconfianza'),
                ('Indiferencia', 'Indiferencia'),
            ]),
            'confianza_expertos': forms.Select(choices=[
                ('Confianza', 'Confianza'),
                ('Indiferencia', 'Indiferencia'),
                ('Desconfianza', 'Desconfianza'),
            ]),
            'reaccion_bonos': forms.Select(choices=[
                ('Disminuiria', 'Disminuiria mi apoyo (prefiero la estabilidad economica antes que mas bonos)'),
                ('No cambiaria', 'No cambiaria mi desicion'),
                ('Aumentaria', 'Aumentaria mi apoyo (los bonos benefician a la poblacion)'),
                ('Sin opinion', 'No tengo opinion'),
            ]),
        }

class EncuestaCreateView(CreateView):
    model = Encuesta
    form_class = EncuestaForm
    template_name = 'encuesta/encuesta_form.html'
    success_url = reverse_lazy('encuesta:success')

class EncuestaSuccessView(TemplateView):
    template_name = 'encuesta/encuesta_success.html'

@method_decorator(staff_member_required, name='dispatch')
class ExcelExportView(TemplateView):
    template_name = 'encuesta/excel_export.html'

@method_decorator(staff_member_required, name='dispatch')
class DownloadExcelView(View):
    def get(self, request):
        # Get all survey data
        encuestas = Encuesta.objects.all()
        
        # Create a DataFrame with all the survey data
        data = []
        for encuesta in encuestas:
            encuesta_dict = {}
            # Get all fields from the model
            for field in Encuesta._meta.get_fields():
                if field.name != 'id':
                    value = getattr(encuesta, field.name)
                    # Convert datetime with timezone to naive datetime
                    if isinstance(value, datetime.datetime) and value.tzinfo is not None:
                        value = value.replace(tzinfo=None)
                    encuesta_dict[field.verbose_name or field.name] = value
            data.append(encuesta_dict)
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Create response with Excel file
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="encuestas.xlsx"'
        
        # Create Excel file
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Encuestas')
            
            # Get the workbook and the worksheet
            workbook = writer.book
            worksheet = writer.sheets['Encuestas']
            
            # Format header row
            header_font = Font(bold=True, color='FFFFFF')
            header_fill = PatternFill(start_color='366092', end_color='366092', fill_type='solid')
            header_alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
            
            # Apply formatting to header row
            for cell in worksheet[1]:
                cell.font = header_font
                cell.fill = header_fill
                cell.alignment = header_alignment
            
            # Auto-adjust column width
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = (max_length + 2) * 1.2
                worksheet.column_dimensions[column_letter].width = adjusted_width
        
        return response
