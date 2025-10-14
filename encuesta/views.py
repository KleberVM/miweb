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
from django.db import connection

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
            # Get all fields from the model using field names (not verbose_name)
            for field in Encuesta._meta.get_fields():
                if field.name not in ['id', 'created_at']:
                    value = getattr(encuesta, field.name)
                    # Convert datetime with timezone to naive datetime
                    if isinstance(value, datetime.datetime) and value.tzinfo is not None:
                        value = value.replace(tzinfo=None)
                    # Use field.name instead of verbose_name for consistency
                    encuesta_dict[field.name] = value
            data.append(encuesta_dict)
        
        # Create DataFrame with specific column order
        column_order = [
            'nombre', 'correo', 'edad', 'genero', 'ciudad', 'localidad',
            'situacion_educativa', 'profesion_carrera', 'estrato_socioeconomico',
            'estatus_laboral', 'contribuye_familia', 'nivel_ingreso',
            'intencion_voto', 'firmeza_voto', 'alineamiento_ideologico',
            'influencia_entorno', 'motivacion_voto', 'estabilidad', 'empleo',
            'deuda', 'calidad', 'becas', 'corrupcion_justicia', 'salud',
            'seguridad_ciudadana', 'cambio_climatico', 'temaGenero',
            'derechos_sociales', 'modelo_desarrollo', 'PropuestaCandidatoNegativo',
            'descontentoCandidato', 'experiencia_gestion_paz', 'honestidad_paz',
            'capacidad_unir_paz', 'conexion_jovenes_paz', 'liderazgo_paz',
            'propuestas_claras_paz', 'experiencia_gestion_tuto', 'honestidad_tuto',
            'capacidad_unir_tuto', 'conexion_jovenes_tuto', 'liderazgo_tuto',
            'propuestas_claras_tuto', 'medio_influencia', 'confianza_redes',
            'conocimiento_economico', 'influencia_imagen', 'cambio_opinion_debates',
            'optimismo_futuro', 'emocion_dominante', 'percepcion_eficacia',
            'confianza_expertos', 'reaccion_escandalo', 'reaccion_bonos'
        ]
        
        if data:
            df = pd.DataFrame(data)
            # Reorder columns
            df = df[column_order]
        else:
            # Create empty DataFrame with column headers if no data
            df = pd.DataFrame(columns=column_order)
        
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

@method_decorator(staff_member_required, name='dispatch')
class ExcelUploadView(TemplateView):
    template_name = 'encuesta/excel_upload.html'

@method_decorator(staff_member_required, name='dispatch')
class ProcessExcelUploadView(View):
    def post(self, request):
        if 'excel_file' not in request.FILES:
            return render(request, 'encuesta/excel_upload.html', {
                'error': 'No se ha seleccionado ningún archivo.'
            })
        
        excel_file = request.FILES['excel_file']
        
        # Validar que sea un archivo Excel
        if not excel_file.name.endswith(('.xlsx', '.xls')):
            return render(request, 'encuesta/excel_upload.html', {
                'error': 'El archivo debe ser un archivo Excel (.xlsx o .xls).'
            })
        
        try:
            # Cerrar conexión existente para evitar timeout
            connection.close()
            
            # Leer el archivo Excel
            df = pd.read_excel(excel_file)
            
            # Definir las columnas requeridas (en el orden del modelo)
            required_columns = [
                'nombre', 'correo', 'edad', 'genero', 'ciudad', 'localidad',
                'situacion_educativa', 'profesion_carrera', 'estrato_socioeconomico',
                'estatus_laboral', 'contribuye_familia', 'nivel_ingreso',
                'intencion_voto', 'firmeza_voto', 'alineamiento_ideologico',
                'influencia_entorno', 'motivacion_voto', 'estabilidad', 'empleo',
                'deuda', 'calidad', 'becas', 'corrupcion_justicia', 'salud',
                'seguridad_ciudadana', 'cambio_climatico', 'temaGenero',
                'derechos_sociales', 'modelo_desarrollo', 'PropuestaCandidatoNegativo',
                'descontentoCandidato', 'experiencia_gestion_paz', 'honestidad_paz',
                'capacidad_unir_paz', 'conexion_jovenes_paz', 'liderazgo_paz',
                'propuestas_claras_paz', 'experiencia_gestion_tuto', 'honestidad_tuto',
                'capacidad_unir_tuto', 'conexion_jovenes_tuto', 'liderazgo_tuto',
                'propuestas_claras_tuto', 'medio_influencia', 'confianza_redes',
                'conocimiento_economico', 'influencia_imagen', 'cambio_opinion_debates',
                'optimismo_futuro', 'emocion_dominante', 'percepcion_eficacia',
                'confianza_expertos', 'reaccion_escandalo', 'reaccion_bonos'
            ]
            
            # Verificar que todas las columnas requeridas estén presentes
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                return render(request, 'encuesta/excel_upload.html', {
                    'error': f'Faltan las siguientes columnas en el archivo Excel: {", ".join(missing_columns)}'
                })
            
            # Procesar cada fila (omitiendo la primera fila que son los encabezados)
            success_count = 0
            error_count = 0
            errors = []
            
            # Procesar en lotes para evitar timeout
            batch_size = 50
            encuestas_batch = []
            
            for index, row in df.iterrows():
                try:
                    # Crear instancia de Encuesta
                    encuesta = Encuesta(
                        nombre=row['nombre'] if pd.notna(row['nombre']) else None,
                        correo=row['correo'] if pd.notna(row['correo']) else None,
                        edad=str(row['edad']),
                        genero=str(row['genero']),
                        ciudad=str(row['ciudad']),
                        localidad=str(row['localidad']),
                        situacion_educativa=str(row['situacion_educativa']),
                        profesion_carrera=row['profesion_carrera'] if pd.notna(row['profesion_carrera']) else None,
                        estrato_socioeconomico=str(row['estrato_socioeconomico']),
                        estatus_laboral=str(row['estatus_laboral']),
                        contribuye_familia=str(row['contribuye_familia']),
                        nivel_ingreso=str(row['nivel_ingreso']),
                        intencion_voto=str(row['intencion_voto']),
                        firmeza_voto=int(row['firmeza_voto']),
                        alineamiento_ideologico=str(row['alineamiento_ideologico']),
                        influencia_entorno=int(row['influencia_entorno']),
                        motivacion_voto=str(row['motivacion_voto']),
                        estabilidad=int(row['estabilidad']),
                        empleo=int(row['empleo']),
                        deuda=int(row['deuda']),
                        calidad=int(row['calidad']),
                        becas=int(row['becas']),
                        corrupcion_justicia=int(row['corrupcion_justicia']),
                        salud=int(row['salud']),
                        seguridad_ciudadana=int(row['seguridad_ciudadana']),
                        cambio_climatico=int(row['cambio_climatico']),
                        temaGenero=int(row['temaGenero']),
                        derechos_sociales=int(row['derechos_sociales']),
                        modelo_desarrollo=int(row['modelo_desarrollo']),
                        PropuestaCandidatoNegativo=int(row['PropuestaCandidatoNegativo']),
                        descontentoCandidato=int(row['descontentoCandidato']),
                        experiencia_gestion_paz=int(row['experiencia_gestion_paz']),
                        honestidad_paz=int(row['honestidad_paz']),
                        capacidad_unir_paz=int(row['capacidad_unir_paz']),
                        conexion_jovenes_paz=int(row['conexion_jovenes_paz']),
                        liderazgo_paz=int(row['liderazgo_paz']),
                        propuestas_claras_paz=int(row['propuestas_claras_paz']),
                        experiencia_gestion_tuto=int(row['experiencia_gestion_tuto']),
                        honestidad_tuto=int(row['honestidad_tuto']),
                        capacidad_unir_tuto=int(row['capacidad_unir_tuto']),
                        conexion_jovenes_tuto=int(row['conexion_jovenes_tuto']),
                        liderazgo_tuto=int(row['liderazgo_tuto']),
                        propuestas_claras_tuto=int(row['propuestas_claras_tuto']),
                        medio_influencia=str(row['medio_influencia']),
                        confianza_redes=int(row['confianza_redes']),
                        conocimiento_economico=str(row['conocimiento_economico']),
                        influencia_imagen=int(row['influencia_imagen']),
                        cambio_opinion_debates=str(row['cambio_opinion_debates']),
                        optimismo_futuro=int(row['optimismo_futuro']),
                        emocion_dominante=str(row['emocion_dominante']),
                        percepcion_eficacia=str(row['percepcion_eficacia']),
                        confianza_expertos=str(row['confianza_expertos']),
                        reaccion_escandalo=int(row['reaccion_escandalo']),
                        reaccion_bonos=str(row['reaccion_bonos'])
                    )
                    encuestas_batch.append(encuesta)
                    
                    # Guardar en lotes
                    if len(encuestas_batch) >= batch_size:
                        Encuesta.objects.bulk_create(encuestas_batch)
                        success_count += len(encuestas_batch)
                        encuestas_batch = []
                        
                except Exception as e:
                    error_count += 1
                    errors.append(f'Fila {index + 2}: {str(e)}')
            
            # Guardar el último lote si queda algo
            if encuestas_batch:
                try:
                    Encuesta.objects.bulk_create(encuestas_batch)
                    success_count += len(encuestas_batch)
                except Exception as e:
                    error_count += len(encuestas_batch)
                    errors.append(f'Error al guardar último lote: {str(e)}')
            
            # Preparar mensaje de resultado
            if error_count == 0:
                message = f'¡Éxito! Se importaron {success_count} encuestas correctamente.'
                message_type = 'success'
            else:
                message = f'Se importaron {success_count} encuestas. {error_count} filas tuvieron errores.'
                message_type = 'warning'
            
            return render(request, 'encuesta/excel_upload.html', {
                'message': message,
                'message_type': message_type,
                'success_count': success_count,
                'error_count': error_count,
                'errors': errors[:10]  # Mostrar solo los primeros 10 errores
            })
            
        except Exception as e:
            return render(request, 'encuesta/excel_upload.html', {
                'error': f'Error al procesar el archivo: {str(e)}'
            })

@method_decorator(staff_member_required, name='dispatch')
class DeleteAllEncuestasView(View):
    def post(self, request):
        try:
            # Contar cuántas encuestas hay antes de borrar
            count = Encuesta.objects.count()
            
            # Borrar todas las encuestas
            Encuesta.objects.all().delete()
            
            return render(request, 'encuesta/excel_upload.html', {
                'message': f'Se eliminaron exitosamente {count} encuestas de la base de datos.',
                'message_type': 'success'
            })
        except Exception as e:
            return render(request, 'encuesta/excel_upload.html', {
                'error': f'Error al eliminar las encuestas: {str(e)}'
            })
