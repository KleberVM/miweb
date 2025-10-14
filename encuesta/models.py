from django.db import models

# Create your models here.
from django.db import models

# ------------------------------
# Sección 1: Datos Demográficos y Socioeconómicos
# ------------------------------
class Encuesta(models.Model):
    # Datos personales básicos

    nombre = models.CharField(max_length=100,blank=True, null=True)
    correo = models.EmailField(unique=False, blank=True, null=True)

    edad = models.CharField(
        max_length=10,
        choices=[
            ('18-24', '18-24'),
            ('25-30', '25-30'),
        ]
    )
    genero = models.CharField(
        max_length=20,
        choices=[
            ('Masculino', 'Masculino'),
            ('Femenino', 'Femenino'),
            ('No Binario', 'No Binario'),
            ('Prefiero no decir', 'Prefiero no decir'),
        ]
    )
    ciudad = models.CharField(
        max_length=50,
        choices=[
            ('La Paz', 'La Paz'),
            ('Cochabamba', 'Cochabamba'),
            ('Santa Cruz', 'Santa Cruz'),
            ('Oruro', 'Oruro'),
            ('Potosí', 'Potosí'),
            ('Chuquisaca', 'Chuquisaca'),
            ('Tarija', 'Tarija'),
            ('Beni', 'Beni'),
            ('Pando', 'Pando'),
        ]
    )
    localidad = models.CharField(max_length=50)
    situacion_educativa = models.CharField(
        max_length=100,
        choices=[
            ('Estudiante Universitario', 'Estudiante Universitario'),
            ('Recien Profecionalizado', 'Recien Profecionalizado'),
        ]
    )
    profesion_carrera = models.CharField(max_length=100, blank=True, null=True)
    estrato_socioeconomico = models.CharField(
        max_length=20,
        choices=[
            ('Bajo', 'Bajo'),
            ('Medio-Bajo', 'Medio-Bajo'),
            ('Medio', 'Medio'),
            ('Medio-Alto', 'Medio-Alto'),
        ]
    )
    estatus_laboral = models.CharField(
        max_length=50,
        choices=[
            ('Empleado Publica', 'Empleado Institución Pública'),
            ('Empleado Privada', 'Empleado Empresa Privada'),
            ('Desempleado', 'Desempleado'),
            ('Emprendedor', 'Emprendedor'),
            ('Freelance', 'Freelance'),
            ('Innovador', 'Innovador'),
        ]
    )
    contribuye_familia = models.CharField(
        max_length=20,
        choices=[
            ('Si, completamente', 'Sí, completamente'),
            ('Si, parcialmente', 'Sí, parcialmente'),
            ('No', 'No, aún no'),
        ]
    )
    nivel_ingreso = models.CharField(
        max_length=20,
        choices=[
            ('Sin ingresos', 'Sin ingresos'),
            ('Bajos', 'Ingresos bajos'),
            ('Medios', 'Ingresos medios'),
            ('Altos', 'Ingresos altos'),
        ]
    )

    # ------------------------------
    # Sección 2: Intención de voto y alineamiento ideológico
    # ------------------------------
    intencion_voto = models.CharField(
        max_length=50,
        choices=[
            ('Rodrigo Paz Pereira', 'Rodrigo Paz Pereira'),
            ('Jorge Quiroga Ramírez', 'Jorge Quiroga Ramírez'),
            ('Blanco', 'Voto Blanco'),
            ('Nulo', 'Voto Nulo'),
            ('Indeciso', 'Aún no lo decido'),
        ]
    )
    firmeza_voto = models.IntegerField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    )  # 1-5
    alineamiento_ideologico = models.CharField(
        max_length=30,
        choices=[
            ('Izquierda/Progresista', 'Izquierda/Progresista'),
            ('Centro-Izquierda', 'Centro-Izquierda'),
            ('Centro', 'Centro'),
            ('Centro-Derecha', 'Centro-Derecha'),
            ('Derecha Conservadora', 'Derecha Conservadora'),
        ]
    )
    influencia_entorno = models.IntegerField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    )  # 1-5
    motivacion_voto = models.CharField(
        max_length=100,
        choices=[
            ('Las propuestas del candidato', 'Las propuestas del candidato'),
            ('Su experiencia o trayectoria', 'Su experiencia o trayectoria'),
            ('Su ideología o valores', 'Su ideología o valores'),
            ('El rechazo al otro candidato', 'El rechazo al otro candidato'),
            ('Opiniones de su entorno', 'Opiniones de su entorno'),
            ('Ninguna', 'Ninguna'),
        ]
    )

    # ------------------------------
    # Sección 3: Factores de decisión
    # ------------------------------
    estabilidad = models.IntegerField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    )  # 1-5
    empleo = models.IntegerField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    )  # 1-5
    deuda = models.IntegerField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    )  # 1-5

    calidad = models.IntegerField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    )  # 1-5
    becas = models.IntegerField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    )  # 1-5

    corrupcion_justicia = models.IntegerField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    )  # 1-5
    salud = models.IntegerField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    )  # 1-5

    seguridad_ciudadana = models.IntegerField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    )  # 1-5

    cambio_climatico = models.IntegerField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    )  # 1-5

    temaGenero = models.IntegerField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    )  # 1-5

    derechos_sociales = models.IntegerField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    )  # 1-5

    modelo_desarrollo = models.IntegerField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    )  # 1-5

    PropuestaCandidatoNegativo = models.IntegerField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    )  # 1-5
    descontentoCandidato = models.IntegerField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    )  # 1-5

    # ------------------------------
    # Sección 4: Percepción de candidatos y atributos
    # ------------------------------
    #para rodrigo paz
    experiencia_gestion_paz = models.IntegerField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    )  # 1-5
    honestidad_paz = models.IntegerField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    )  # 1-5
    capacidad_unir_paz = models.IntegerField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    )  # 1-5
    conexion_jovenes_paz = models.IntegerField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    )  # 1-5
    liderazgo_paz = models.IntegerField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    )  # 1-5
    propuestas_claras_paz = models.IntegerField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    )  # 1-5
    #para tuto quiroga
    experiencia_gestion_tuto = models.IntegerField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    )  # 1-5
    honestidad_tuto = models.IntegerField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    )  # 1-5
    capacidad_unir_tuto = models.IntegerField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    )  # 1-5
    conexion_jovenes_tuto = models.IntegerField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    )  # 1-5
    liderazgo_tuto = models.IntegerField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    )  # 1-5
    propuestas_claras_tuto = models.IntegerField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    )  # 1-5
    # resto de preguntas
    medio_influencia = models.CharField(
        max_length=100,
        choices=[
            ('Redes Sociales', 'Redes Sociales: TikTok, Facebook, Instagram'),
            ('Medios Comunicacionales', 'Medios Comunicacionales: Televisión tradicional, Radio tradicional'),
            ('Medios Digitales', 'Medios Digitales: Prensa en línea'),
            ('Vínculos sociales', 'Vínculos sociales: Familiares, Amigos'),
        ]
    )
    confianza_redes = models.IntegerField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    )  # 1-5
    conocimiento_economico = models.CharField(
        max_length=100,
        choices=[
            ('Conocimiento profundo', 'Debe tener un conocimiento profundo del tema'),
            ('Delegar en expertos', 'Es suficiente con que sepa elegir y delegar en buenos expertos'),
        ]
    )
    influencia_imagen = models.IntegerField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    )  # 1-5
    cambio_opinion_debates = models.CharField(
        max_length=5,
        choices=[
            ('Si', 'Sí'),
            ('No', 'No'),
        ]
    )

    # ------------------------------
    # Sección 5: Impacto emocional y percepción de futuro
    # ------------------------------
    optimismo_futuro = models.IntegerField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    )  # 1-5
    emocion_dominante = models.CharField(
        max_length=50,
        choices=[
            ('Esperanza', 'Esperanza'),
            ('Temor', 'Temor'),
            ('Desconfianza', 'Desconfianza'),
            ('Indiferencia', 'Indiferencia'),
        ]
    )
    percepcion_eficacia = models.CharField(
        max_length=5,
        choices=[
            ('Si', 'Sí'),
            ('No', 'No'),
        ]
    )

    # ------------------------------
    # Sección 6: Escenarios hipotéticos de simulación
    # ------------------------------
    confianza_expertos = models.CharField(
        max_length=50,
        choices=[
            ('Confianza', 'Confianza'),
            ('Indiferencia', 'Indiferencia'),
            ('Desconfianza', 'Desconfianza'),
        ]
    )
    reaccion_escandalo = models.IntegerField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    )  # 1-5
    reaccion_bonos = models.CharField(
        max_length=100,
        choices=[
            ('Disminuiria', 'Disminuiria mi apoyo (prefiero la estabilidad economica antes que mas bonos)'),
            ('No cambiaria', 'No cambiaria mi desicion'),
            ('Aumentaria', 'Aumentaria mi apoyo (los bonos benefician a la poblacion)'),
            ('Sin opinion', 'No tengo opinion'),
        ]
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Encuesta #{self.id} - Edad: {self.edad} - Ciudad: {self.ciudad}"
