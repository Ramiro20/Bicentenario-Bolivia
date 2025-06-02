from django.db import models
from django.contrib.auth.models import AbstractUser
import os
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from cities_light.models import City, Country
from django.core.validators import MinValueValidator
from decimal import Decimal

class Usuario(AbstractUser):
    GENERO_OPCIONES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
        ('N', 'Prefiero no decir'),
    ]
    
    email = models.EmailField('Correo Electrónico', unique=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    genero = models.CharField(max_length=1, choices=GENERO_OPCIONES, blank=True, null=True)
    numero_telefono = models.CharField(max_length=20, blank=True, null=True)
    pais = CountryField(blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True) 
    es_eventos = models.BooleanField(default=False)
    es_cultural = models.BooleanField(default=False)
    es_sistema = models.BooleanField(default=False)
    email_confirmado = models.BooleanField(default=False)
    codigo_confirmacion = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

class Fuente(models.Model):
    referencia = models.TextField()
    url = models.URLField(blank=True, null=True)

class Multimedia(models.Model):
    archivo = models.FileField(upload_to='multimedia/')
    tipo = models.CharField(max_length=50, choices=[
        ('imagen', 'Imagen'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('documento', 'Documento'),
    ])
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return f"{self.tipo} - {self.archivo.name}"
class Historia(models.Model):
    TIPO_CHOICES = [
        ('batalla', 'Batalla'),
        ('independencia', 'Independencia'),
        ('personaje', 'Personaje'),
        ('otro', 'Otro'),
    ]

    nombre = models.CharField(max_length=255)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='otro')
    descripcion = models.TextField()
    fecha = models.DateField()
    multimedia = models.ManyToManyField(Multimedia, related_name='historias', blank=True)
    fuente = models.ManyToManyField(Fuente, related_name='fuentes', blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"


class Independencia(models.Model):
    nombre = models.CharField(max_length=255)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    imagen = models.ImageField(upload_to='independencias/', null=True, blank=True)
    descripcion = models.TextField()
    historia = models.ForeignKey(Historia, on_delete=models.CASCADE)

class Presidente(models.Model):
    nombre = models.CharField(max_length=255)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    lugar_nacimiento = models.CharField(max_length=255)
    descripcion = models.TextField()
    partido = models.CharField(max_length=255)
    educacion = models.CharField(max_length=255)
    profesion = models.CharField(max_length=255)
    mandato = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='presidentes/', null=True, blank=True)
    historia = models.ForeignKey(Historia, on_delete=models.CASCADE)

class Comentario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_comentario = models.DateField()
    archivo = models.ImageField(upload_to='comentarios/', null=True, blank=True)


class Noticia(models.Model):
    titulo = models.CharField(max_length=255)
    contenido = models.TextField()
    fecha_publicacion = models.DateField(auto_now_add=True)
    autor = models.CharField(max_length=255)
    multimedia = models.ManyToManyField(Multimedia, related_name='noticias', blank=True)

    def __str__(self):
        return self.titulo


class Presentacion(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    archivo = models.ImageField(upload_to='presentaciones/', null=True, blank=True)

#EVENTOS

class CategoriaEvento(models.TextChoices):
    CULTURAL = 'Cultural'
    DEPORTIVO = 'Deportivo'
    GASTRONOMICO = 'Gastronomico'
    ACADEMICO = 'Academico'
    FERIA = 'Feria'
    SOCIAL = 'Social'

class ModalidadEvento(models.TextChoices):
    PRESENCIAL = 'Presencial'
    VIRTUAL = 'Virtual'
    MIXTO = 'Mixto'

class TipoPublico(models.TextChoices):
    INFANTIL = 'Infantil'
    JUVENIL = 'Juvenil'
    ADULTO = 'Adulto'
    GENERAL = 'General'

class DepartamentoBolivia(models.TextChoices):
    CHUQUISACA = 'Chuquisaca', 'Chuquisaca'
    LA_PAZ = 'La Paz', 'La Paz'
    COCHABAMBA = 'Cochabamba', 'Cochabamba'
    ORURO = 'Oruro', 'Oruro'
    POTOSI = 'Potosí', 'Potosí'
    TARIJA = 'Tarija', 'Tarija'
    SANTA_CRUZ = 'Santa Cruz', 'Santa Cruz'
    BENI = 'Beni', 'Beni'
    PANDO = 'Pando', 'Pando'

# --- Funciones dinámicas para carpetas de imagen ---

def logo_patrocinador_path(instance, filename):
    nombre = slugify(instance.nombre)
    ext = os.path.splitext(filename)[1]
    return f'patrocinadores/{nombre}/logo{ext}'

def evento_imagen_principal_path(instance, filename):
    nombre = slugify(instance.titulo)
    ext = os.path.splitext(filename)[1]
    return f'eventos/{nombre}/principal{ext}'

def imagen_evento_path(instance, filename):
    nombre_evento = slugify(instance.evento.titulo)
    return f'eventos/{nombre_evento}/galeria/{filename}'

# --- Entidades del sistema ---

class Lugar(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    departamento = models.CharField(max_length=20, choices=DepartamentoBolivia.choices)
    latitud = models.FloatField()  # Guardar la latitud como un número flotante
    longitud = models.FloatField()  # Guardar la longitud como un número flotante

    def __str__(self):
        return f"{self.nombre} - {self.departamento}"

    def get_coordenadas(self):
        return f"{self.latitud}, {self.longitud}"
    
class Patrocinador(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to=logo_patrocinador_path, blank=True, null=True)

    def __str__(self):
        return self.nombre
    
class PatrocinadorPagina(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to=logo_patrocinador_path, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Recurso(models.Model):
    TIPO_RECURSO = [
        ('Material', 'Material'),
        ('Tecnológico', 'Tecnológico'),
        ('Humano', 'Humano'),
    ]

    tipo = models.CharField(max_length=20, choices=TIPO_RECURSO)
    descripcion = models.TextField()

    def __str__(self):
        return f"{self.tipo}: {self.descripcion[:30]}..."

class Expositor(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    img = models.ImageField(upload_to='expositores/', null=True, blank=True)

    def __str__(self):
        return self.nombre
    
class EnlaceEvento(models.Model):
    nombre = models.CharField(max_length=100, help_text="Nombre descriptivo del enlace, ej. Zoom principal")
    url = models.URLField(help_text="URL del enlace")

    def __str__(self):
        return f"{self.nombre} - {self.url}"

class Evento(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    capacidad = models.PositiveIntegerField()
    modalidad = models.CharField(max_length=10, choices=ModalidadEvento.choices)
    categoria = models.CharField(max_length=20, choices=CategoriaEvento.choices)
    tipo_publico = models.CharField(max_length=10, choices=TipoPublico.choices)
    
    lugar = models.ForeignKey(Lugar, on_delete=models.CASCADE, related_name='eventos')
    imagen_principal = models.ImageField(upload_to=evento_imagen_principal_path, blank=True, null=True)

    patrocinadores = models.ManyToManyField(Patrocinador, related_name='eventos', blank=True)
    expositores = models.ManyToManyField(Expositor, related_name='eventos', blank=True)
    recursos = models.ManyToManyField(Recurso, related_name='eventos', blank=True)
    
    enlaces = models.ManyToManyField(EnlaceEvento, related_name='eventos', blank=True)

    # Nuevo: indica si es gratuito
    es_gratuito = models.BooleanField(default=True)
    
    # Nuevo: precio si es de paga
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        blank=True,
        null=True
    )
    # Relación con el usuario
    usuario_creador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='eventos_creados')
    def __str__(self):
        return self.titulo
class Convocatoria(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='convocatorias/', blank=True, null=True)
    archivo_pdf = models.FileField(upload_to='convocatorias/pdfs/', blank=True, null=True)
    fecha_publicacion = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.titulo
class ImagenEvento(models.Model):
    evento = models.ForeignKey(Evento, related_name='imagenes', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to=imagen_evento_path)
    descripcion = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Imagen de {self.evento.titulo}"
    
# consejo nacional

class ConsejoNacional(models.Model):
    nombre = models.CharField(max_length=200)
    cargo = models.CharField(max_length=100)
    descripcion = models.TextField()
    foto = models.ImageField(upload_to='consejo_fotos/')

    def __str__(self):
        return f"{self.nombre} - {self.cargo}"

#CULTURAL

class Museo(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    lugar = models.ForeignKey(Lugar, on_delete=models.SET_NULL, null=True, blank=True)
    multimedia = models.ManyToManyField(Multimedia, related_name='museos', blank=True)
    fuente = models.ManyToManyField(Fuente, related_name='museos', blank=True)

    def __str__(self):
        return self.nombre

class Turismo(models.Model):

    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    lugar = models.ForeignKey(Lugar, on_delete=models.SET_NULL, null=True, blank=True)
    multimedia = models.ManyToManyField(Multimedia, related_name='turismo', blank=True)
    fuente = models.ManyToManyField(Fuente, related_name='turismo', blank=True)

    def __str__(self):
        return self.nombre
    
class ArteYArtesania(models.Model):
    nombre = models.CharField(max_length=255)
    origen = models.CharField(max_length=255)
    descripcion = models.TextField()
    multimedia = models.ManyToManyField(Multimedia, related_name='artes_y_artesanias', blank=True)
    fuente = models.ManyToManyField(Fuente, related_name='artes_y_artesanias', blank=True)

    def __str__(self):
        return f"{self.nombre})"

class Etnia(models.Model):
    nombre = models.CharField(max_length=255)
    lenguaje = models.CharField(max_length=255)
    costumbres = models.TextField()
    multimedia = models.ManyToManyField(Multimedia, related_name='etnias', blank=True)
    fuente = models.ManyToManyField(Fuente, related_name='etnias', blank=True)

    def __str__(self):
        return self.nombre
