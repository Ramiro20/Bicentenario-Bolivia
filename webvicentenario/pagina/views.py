from django.shortcuts import render
from django.core.paginator import Paginator
from .models import *
from datetime import datetime
from django.http import JsonResponse
from django.core import serializers

def index(request):
    eventos = Evento.objects.order_by('-fecha_inicio')[:3] 
    patrocinadores = PatrocinadorPagina.objects.all()
    return render(request, 'index.html', {
        'eventos': eventos,
        'patrocinadores': patrocinadores,
    })


def buscar_eventos_por_fecha(request):
    eventos = []
    resumen = {}
    modPresencial = 0
    modMixto = 0
    modVirtual = 0

    if request.method == 'GET':
        fecha_inicio = request.GET.get('fecha_inicio')
        fecha_fin = request.GET.get('fecha_fin')

        if fecha_inicio and fecha_fin:
            try:
                fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
                fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()

                categorias = ["Academico", "Deportivo", "Feria", "Gastronomico", "Cultural", "Social"]
                eventos = Evento.objects.filter(
                    categoria__in=categorias,
                    fecha_inicio__gte=fecha_inicio,
                    fecha_fin__lte=fecha_fin
                ).order_by('fecha_inicio')

                # Contadores
                resumen = {
                    "Academico": 0,
                    "Deportivo": 0,
                    "Feria": 0,
                    "Gastronomico": 0,
                    "Cultural": 0,
                    "Social": 0,
                }

                for evento in eventos:
                    if evento.categoria in resumen:
                        resumen[evento.categoria] += 1

                for evento in eventos:
                    if evento.modalidad == "Presencial":
                        modPresencial += 1
                    if evento.modalidad == "Mixto":
                        modMixto += 1
                    if evento.modalidad == "Virtual":
                        modVirtual += 1

            except ValueError:
                pass  # manejar error si es necesario

    return render(request, 'eventos_filtrados.html', {
        'eventos': eventos,
        'resumen': resumen,
        'modPresencial' : modPresencial,
        'modMixto' : modMixto,
        'modVirtual' : modVirtual
    })

def consejo(request):
    consejo = ConsejoNacional.objects.all()
    return render(request, 'consejo.html', {'consejo': consejo})

def generar_qr(texto):
    """
    Genera un código QR en formato PNG y lo devuelve como un objeto File listo para guardar.
    """
    qr = qrcode.make(texto)
    buffer = BytesIO()
    qr.save(buffer, format='PNG')
    buffer.seek(0)
    return File(buffer, name='qr.png')


def batallas(request):
    eventos = Historia.objects.filter(tipo='batalla').order_by('-fecha')   
    paginator = Paginator(eventos, 6) 
    page_number = request.GET.get('page')  
    eventos_page = paginator.get_page(page_number)  

    return render(request, 'batallas.html', {'eventos': eventos_page})

def independencias(request):
    eventos = Historia.objects.filter(tipo='independencia').order_by('-fecha')
    paginator = Paginator(eventos, 6)
    page_number = request.GET.get('page')
    eventos_paginated = paginator.get_page(page_number)

    return render(request, 'independencias.html', {'eventos': eventos_paginated})

def personajes(request):
    eventos = Historia.objects.filter(tipo='personaje').order_by('-fecha')

    paginator = Paginator(eventos, 6)  
    page_number = request.GET.get('page')
    eventos_paginated = paginator.get_page(page_number)

    return render(request, 'personajes.html', {'eventos': eventos_paginated})

def presidentes(request):

    eventos = Presidente.objects.all().order_by('-fecha_nacimiento')
    paginator = Paginator(eventos, 6) 
    page_number = request.GET.get('page')
    eventos_paginated = paginator.get_page(page_number)

    return render(request, 'presidentes.html', {'eventos': eventos_paginated})

def museos(request):
    lista_museos = Museo.objects.all().order_by('nombre')
    paginator = Paginator(lista_museos, 6)  # 6 museos por página
    page = request.GET.get('page')
    museos_paginados = paginator.get_page(page)

    return render(request, 'museos.html', {'museos': museos_paginados})

def artes(request):
    lista_artes = ArteYArtesania.objects.all().order_by('nombre')
    paginator = Paginator(lista_artes, 6)  # 6 por página
    page = request.GET.get('page')
    artes = paginator.get_page(page)
    return render(request, 'artes.html', {'artes': artes})

def turismo(request):
    lista_turismo = Turismo.objects.all().order_by('nombre')
    paginator = Paginator(lista_turismo, 6)  # 6 por página
    page = request.GET.get('page')
    turismo = paginator.get_page(page)
    return render(request, 'turismo.html', {'turismo': turismo})


def etnias(request):
    lista_etnias = Etnia.objects.all().order_by('nombre')
    paginator = Paginator(lista_etnias, 6)
    page = request.GET.get('page')
    etnias = paginator.get_page(page)
    return render(request, 'etnias.html', {'etnias': etnias})


def academicos(request):
    lista = Evento.objects.filter(categoria='Academico').order_by('-fecha_inicio')
    paginator = Paginator(lista, 6)
    page = request.GET.get('page')
    academicos = paginator.get_page(page)
    return render(request, 'academicos.html', {'academicos': academicos})

def culturales(request):
    lista = Evento.objects.filter(categoria='Cultural').order_by('-fecha_inicio')
    paginator = Paginator(lista, 6)
    page = request.GET.get('page')
    eventos = paginator.get_page(page)
    return render(request, 'culturales.html', {'eventos': eventos})

def gastronomicos(request):
    lista = Evento.objects.filter(categoria='Gastronomico').order_by('-fecha_inicio')
    paginator = Paginator(lista, 6)
    page = request.GET.get('page')
    eventos = paginator.get_page(page)
    return render(request, 'gastronomicos.html', {'eventos': eventos})

def deportivos(request):
    lista = Evento.objects.filter(categoria='Deportivo').order_by('-fecha_inicio')
    paginator = Paginator(lista, 6)
    page = request.GET.get('page')
    eventos = paginator.get_page(page)
    return render(request, 'deportivos.html', {'eventos': eventos})

def feria(request):
    lista = Evento.objects.filter(categoria='Feria').order_by('-fecha_inicio')
    paginator = Paginator(lista, 6)
    page = request.GET.get('page')
    eventos = paginator.get_page(page)
    return render(request, 'feria.html', {'eventos': eventos})

def social(request):
    lista = Evento.objects.filter(categoria='Social').order_by('-fecha_inicio')
    paginator = Paginator(lista, 6)
    page = request.GET.get('page')
    eventos = paginator.get_page(page)
    return render(request, 'social.html', {'eventos': eventos})

def noticias(request):
    lista = Noticia.objects.all().order_by('-fecha_publicacion')
    paginator = Paginator(lista, 6)
    page = request.GET.get('page')
    eventos = paginator.get_page(page)
    return render(request, 'noticias.html', {'eventos': eventos})

def convocatorias(request):
    lista = Convocatoria.objects.all().order_by('-fecha_publicacion')
    paginator = Paginator(lista, 6)
    page = request.GET.get('page')
    eventos = paginator.get_page(page)
    return render(request, 'convocatorias.html', {'eventos': eventos})
def normalizar_texto(texto):
    """
    Reemplaza vocales con acentos por vocales sin acento
    y convierte a minúsculas
    """
    replacements = (
        ('á', 'a'),
        ('é', 'e'),
        ('í', 'i'),
        ('ó', 'o'),
        ('ú', 'u'),
        ('Á', 'a'),
        ('É', 'e'),
        ('Í', 'i'),
        ('Ó', 'o'),
        ('Ú', 'u'),
    )
    texto = texto.lower()
    for a, b in replacements:
        texto = texto.replace(a, b)
    return texto
from django.shortcuts import render
from django.utils import timezone
from collections import OrderedDict
from calendar import Calendar, month_name
from datetime import datetime
from .models import Evento

def agenda(request):
    ahora = timezone.now()
    
    # Obtener todos los eventos ordenados por fecha
    eventos = Evento.objects.all().order_by('fecha_inicio')
    for evento in eventos:
        categoria = evento.categoria.lower()
        evento.categoria_sin_acentos = (
            categoria.replace('á', 'a')
                     .replace('é', 'e')
                     .replace('í', 'i')
                     .replace('ó', 'o')
                     .replace('ú', 'u')
        )
    # Diccionario de meses en español
    MESES_ES = {
        1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
        5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
        9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
    }

    # Manejo de parámetros de filtro
    selected_year = request.GET.get('year', ahora.year)
    selected_month = request.GET.get('month', ahora.month)
    
    try:
        selected_year = int(selected_year)
        selected_month = int(selected_month) if selected_month else None
    except (ValueError, TypeError):
        selected_year = ahora.year
        selected_month = ahora.month

    # Determinar rango de años disponibles
    años_disponibles = set()
    if eventos.exists():
        primer_evento = eventos.first().fecha_inicio.year
        ultimo_evento = eventos.last().fecha_inicio.year
        años_disponibles = set(range(primer_evento, ultimo_evento + 1))
    else:
        años_disponibles = {ahora.year}

    # Organizar eventos por mes y año
    eventos_por_mes = OrderedDict()
    meses_disponibles = set()

    for evento in eventos:
        fecha = evento.fecha_inicio
        clave = (fecha.year, fecha.month)
        meses_disponibles.add(clave)
        
        if clave not in eventos_por_mes:
            eventos_por_mes[clave] = {
                'nombre_mes': MESES_ES[fecha.month],
                'anio': fecha.year,
                'mes_num': fecha.month,
                'eventos': []
            }
        eventos_por_mes[clave]['eventos'].append(evento)

    # Generar datos para el calendario (si hay mes seleccionado)
    calendar_data = None
    if selected_month:
        cal = Calendar()
        month_days = cal.monthdayscalendar(selected_year, selected_month)
        
        days_with_events = []
        for week in month_days:
            week_events = []
            for day in week:
                if day == 0:
                    week_events.append({'day': day, 'events': []})
                    continue
                    
                day_date = datetime(selected_year, selected_month, day).date()
                day_events = [
                    {
                        'id': e.id,
                        'titulo': e.titulo,
                        'categoria': e.get_categoria_display(),
                        'color': e.categoria.lower()
                                .replace('á', 'a')
                                .replace('é', 'e')
                                .replace('í', 'i')
                                .replace('ó', 'o')
                                .replace('ú', 'u'),
                        'pasado': e.fecha_inicio.date() < ahora.date()
                    } 
                    for e in eventos 
                    if e.fecha_inicio.date() == day_date
                ]
                week_events.append({'day': day, 'events': day_events})
            days_with_events.append(week_events)
        
        calendar_data = {
            'month_name': MESES_ES[selected_month],
            'weeks': days_with_events
        }

    # Preparar datos para filtros
    años_filtro = sorted(años_disponibles, reverse=True)
    
    meses_filtro = []
    for year, month in sorted(meses_disponibles):
        if year == selected_year:
            meses_filtro.append({
                'value': month,
                'nombre': MESES_ES[month],
                'selected': month == selected_month
            })
    categorias_originales = Evento._meta.get_field('categoria').choices
    categorias_normalizadas = [
        (normalizar_texto(value), label) for value, label in categorias_originales
    ]
    context = {
        'eventos_por_mes': list(eventos_por_mes.values()),
        'current_year': ahora.year,
        'current_month': ahora.month,
        'selected_year': selected_year,
        'selected_month': selected_month,
        'calendar': calendar_data,
        'años_filtro': años_filtro,
        'meses_filtro': meses_filtro,
        'categorias': categorias_normalizadas,
        'hoy': ahora.date(),
        'MESES_ES': MESES_ES
    }
    
    return render(request, 'agenda.html', context)


def contactos(request):
    return render(request, 'contactos.html')


def evento_detalle(request, evento_id):
    evento = Evento.objects.prefetch_related('imagenes').get(id=evento_id)
    return render(request, 'evento_detalle.html', {'evento': evento})


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
import json
from django.http import HttpResponse

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        captcha_hash = request.POST.get('captcha_hash')
        captcha_response = request.POST.get('captcha_response')
        
        # Verify CAPTCHA first
        if not CaptchaStore.objects.filter(hashkey=captcha_hash, response=captcha_response.lower()).exists():
            messages.error(request, 'CAPTCHA incorrecto')
            return render(request, 'login.html', {'new_captcha': get_new_captcha()})
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            return redirect('index')  
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
            return render(request, 'login.html', {'new_captcha': get_new_captcha()})
    
    return render(request, 'login.html', {'new_captcha': get_new_captcha()})

def get_new_captcha():
    new_key = CaptchaStore.generate_key()
    new_image = captcha_image_url(new_key)
    return {'key': new_key, 'image': new_image}

def refresh_captcha(request):
    new_captcha = get_new_captcha()
    return HttpResponse(json.dumps(new_captcha), content_type='application/json')







from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.http import require_GET  # Permite solo GET

@require_GET  # Ahora solo acepta GET
def custom_logout(request):
    logout(request)
    return redirect('index')








from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Evento, Lugar, Patrocinador, Recurso, ImagenEvento, CategoriaEvento, ModalidadEvento, TipoPublico, DepartamentoBolivia
from django.utils.text import slugify
import os

@login_required(login_url='index')
def academicoscrud(request):
    # Listar todos los eventos académicos
    eventos = Evento.objects.filter(categoria=CategoriaEvento.ACADEMICO, usuario_creador=request.user)
    return render(request, 'academicoscrud.html', {'eventos': eventos})

@login_required(login_url='index')
def crear_evento_academico(request):
    if request.method == 'POST':
        try:
            # Procesar datos del lugar
            lugar_nombre = request.POST.get('lugar_nombre')
            lugar_direccion = request.POST.get('lugar_direccion')
            lugar_departamento = request.POST.get('lugar_departamento')
            lugar_latitud = request.POST.get('lugar_latitud')
            lugar_longitud = request.POST.get('lugar_longitud')
            
            lugar = Lugar.objects.create(
                nombre=lugar_nombre,
                direccion=lugar_direccion,
                departamento=lugar_departamento,
                latitud=float(request.POST.get('lugar_latitud', '0').replace(',', '.')),
                longitud=float(request.POST.get('lugar_longitud', '0').replace(',', '.'))
            )
            
            # Procesar datos del evento
            titulo = request.POST.get('titulo')
            descripcion = request.POST.get('descripcion')
            fecha_inicio = request.POST.get('fecha_inicio')
            fecha_fin = request.POST.get('fecha_fin')
            capacidad = request.POST.get('capacidad')
            modalidad = request.POST.get('modalidad')
            tipo_publico = request.POST.get('tipo_publico')
            
            # Nuevos campos: es_gratuito y precio
            es_gratuito = 'es_gratuito' in request.POST
            precio = request.POST.get('precio') if not es_gratuito else None
            
            evento = Evento.objects.create(
                titulo=titulo,
                descripcion=descripcion,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                capacidad=capacidad,
                modalidad=modalidad,
                categoria=CategoriaEvento.ACADEMICO,
                tipo_publico=tipo_publico,
                lugar=lugar,
                usuario_creador=request.user,
                es_gratuito=es_gratuito,
                precio=precio
            )
            
            # Procesar imagen principal si existe
            if 'imagen_principal' in request.FILES:
                evento.imagen_principal = request.FILES['imagen_principal']
                evento.save()
            
            # Procesar patrocinadores si existen
            patrocinadores_ids = request.POST.getlist('patrocinadores')
            for patrocinador_id in patrocinadores_ids:
                patrocinador = Patrocinador.objects.get(id=patrocinador_id)
                evento.patrocinadores.add(patrocinador)

            # Procesar expositores si existen
            expositores_ids = request.POST.getlist('expositores')
            for expositor_id in expositores_ids:
                expositor = Expositor.objects.get(id=expositor_id)
                evento.expositores.add(expositor)
            
            # Procesar recursos si existen
            recursos_descripciones = request.POST.getlist('recursos_descripcion')
            recursos_tipos = request.POST.getlist('recursos_tipo')
            
            for descripcion, tipo in zip(recursos_descripciones, recursos_tipos):
                if descripcion:  # Solo crear si hay descripción
                    recurso = Recurso.objects.create(
                        tipo=tipo,
                        descripcion=descripcion
                    )
                    evento.recursos.add(recurso)
            
            # Procesar enlaces del evento
            enlaces_nombres = request.POST.getlist('enlace_nombre')
            enlaces_urls = request.POST.getlist('enlace_url')
            
            for nombre, url in zip(enlaces_nombres, enlaces_urls):
                if nombre and url:  # Solo crear si hay nombre y URL
                    enlace = EnlaceEvento.objects.create(
                        nombre=nombre,
                        url=url
                    )
                    evento.enlaces.add(enlace)
            
            # Procesar imágenes adicionales si existen
            imagenes = request.FILES.getlist('imagenes_evento')
            for imagen in imagenes:
                ImagenEvento.objects.create(
                    evento=evento,
                    imagen=imagen,
                    descripcion=f"Imagen de {evento.titulo}"
                )
            
            messages.success(request, 'Evento académico creado exitosamente!')
            return redirect('academicoscrud')
        
        except Exception as e:
            print(e)
            messages.error(request, f'Error al crear el evento: {str(e)}')
            return redirect('crear_evento_academico')
    
    # GET request - mostrar formulario
    patrocinadores = Patrocinador.objects.all()
    expositores = Expositor.objects.all()
    context = {
        'modalidades': ModalidadEvento.choices,
        'tipos_publico': TipoPublico.choices,
        'departamentos': DepartamentoBolivia.choices,
        'patrocinadores': patrocinadores,
        'expositores': expositores,
    }
    return render(request, 'crear_evento_academico.html', context)

@login_required(login_url='index')
def editar_evento_academico(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id, usuario_creador=request.user)
    lugar = evento.lugar
    
    if request.method == 'POST':
        try:
            # Procesar datos del lugar
            lugar.nombre = request.POST.get('lugar_nombre')
            lugar.direccion = request.POST.get('lugar_direccion')
            lugar.departamento = request.POST.get('lugar_departamento')
            lugar.latitud = float(request.POST.get('lugar_latitud', '0').replace(',', '.'))
            lugar.longitud = float(request.POST.get('lugar_longitud', '0').replace(',', '.'))
            lugar.save()
            
            # Procesar datos del evento
            evento.titulo = request.POST.get('titulo')
            evento.descripcion = request.POST.get('descripcion')
            evento.fecha_inicio = request.POST.get('fecha_inicio')
            evento.fecha_fin = request.POST.get('fecha_fin')
            evento.capacidad = request.POST.get('capacidad')
            evento.modalidad = request.POST.get('modalidad')
            evento.tipo_publico = request.POST.get('tipo_publico')
            
            # Nuevos campos
            evento.es_gratuito = 'es_gratuito' in request.POST
            evento.precio = request.POST.get('precio') if not evento.es_gratuito else None
            
            # Procesar imagen principal si existe
            if 'imagen_principal' in request.FILES:
                evento.imagen_principal = request.FILES['imagen_principal']
            
            evento.save()
            
            # Procesar patrocinadores
            evento.patrocinadores.clear()
            patrocinadores_ids = request.POST.getlist('patrocinadores')
            for patrocinador_id in patrocinadores_ids:
                patrocinador = Patrocinador.objects.get(id=patrocinador_id)
                evento.patrocinadores.add(patrocinador)

            # Procesar expositores
            evento.expositores.clear()
            expositores_ids = request.POST.getlist('expositores')
            for expositor_id in expositores_ids:
                expositor = Expositor.objects.get(id=expositor_id)
                evento.expositores.add(expositor)
            
            # Procesar recursos
            evento.recursos.all().delete()  # Eliminar recursos existentes
            recursos_descripciones = request.POST.getlist('recursos_descripcion')
            recursos_tipos = request.POST.getlist('recursos_tipo')
            
            for descripcion, tipo in zip(recursos_descripciones, recursos_tipos):
                if descripcion:  # Solo crear si hay descripción
                    recurso = Recurso.objects.create(
                        tipo=tipo,
                        descripcion=descripcion
                    )
                    evento.recursos.add(recurso)
            
            # Procesar enlaces del evento
            evento.enlaces.all().delete()  # Eliminar enlaces existentes
            enlaces_nombres = request.POST.getlist('enlace_nombre')
            enlaces_urls = request.POST.getlist('enlace_url')
            
            for nombre, url in zip(enlaces_nombres, enlaces_urls):
                if nombre and url:  # Solo crear si hay nombre y URL
                    enlace = EnlaceEvento.objects.create(
                        nombre=nombre,
                        url=url
                    )
                    evento.enlaces.add(enlace)
            
            # Procesar imágenes adicionales si existen
            imagenes = request.FILES.getlist('imagenes_evento')
            for imagen in imagenes:
                ImagenEvento.objects.create(
                    evento=evento,
                    imagen=imagen,
                    descripcion=f"Imagen de {evento.titulo}"
                )
            
            messages.success(request, 'Evento académico actualizado exitosamente!')
            return redirect('academicoscrud')
        
        except Exception as e:
            print(e)
            messages.error(request, f'Error al actualizar el evento: {str(e)}')
            return redirect('editar_evento_academico', evento_id=evento.id)
    
    # GET request - mostrar formulario
    patrocinadores = Patrocinador.objects.all()
    expositores = Expositor.objects.all()
    patrocinadores_seleccionados = [p.id for p in evento.patrocinadores.all()]
    expositores_seleccionados = [e.id for e in evento.expositores.all()]
    recursos = evento.recursos.all()
    enlaces = evento.enlaces.all()
    imagenes = evento.imagenes.all()
    
    context = {
        'evento': evento,
        'lugar': lugar,
        'modalidades': ModalidadEvento.choices,
        'tipos_publico': TipoPublico.choices,
        'departamentos': DepartamentoBolivia.choices,
        'patrocinadores': patrocinadores,
        'expositores': expositores,
        'patrocinadores_seleccionados': patrocinadores_seleccionados,
        'expositores_seleccionados': expositores_seleccionados,
        'recursos': recursos,
        'enlaces': enlaces,
        'imagenes': imagenes,
    }
    return render(request, 'editar_evento_academico.html', context)


@login_required(login_url='index')
def eliminar_evento_academico(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id, usuario_creador=request.user)
    
    if request.method == 'POST':
        try:
            # Eliminar el lugar asociado si no está siendo usado por otros eventos
            lugar = evento.lugar
            evento.delete()
            if lugar.eventos.count() == 0:
                lugar.delete()
            
            messages.success(request, 'Evento académico eliminado exitosamente!')
        except Exception as e:
            messages.error(request, f'Error al eliminar el evento: {str(e)}')
        
        return redirect('academicoscrud')
    
    return render(request, 'eliminar_evento_academico.html', {'evento': evento})

@login_required(login_url='index')
def eliminar_imagen_evento(request, imagen_id):
    imagen = get_object_or_404(ImagenEvento, id=imagen_id, evento__usuario_creador=request.user)
    evento_id = imagen.evento.id
    imagen.delete()
    messages.success(request, 'Imagen eliminada exitosamente!')
    return redirect('editar_evento_academico', evento_id=evento_id)

@login_required(login_url='index')
def ver_evento_academico(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id, usuario_creador=request.user)
    context = {
        'evento': evento,
        'lugar': evento.lugar,
        'patrocinadores': evento.patrocinadores.all(),
        'expositores': evento.expositores.all(),
        'recursos': evento.recursos.all(),
        'imagenes': evento.imagenes.all()
    }
    return render(request, 'ver_evento_academico.html', context)





@login_required(login_url='index')
def culturalescrud(request):
    # Listar todos los eventos académicos
    eventos = Evento.objects.filter(categoria=CategoriaEvento.CULTURAL, usuario_creador=request.user)
    return render(request, 'culturalescrud.html', {'eventos': eventos})

@login_required(login_url='index')
def crear_evento_cultural(request):
    if request.method == 'POST':
        try:
            # Procesar datos del lugar
            lugar_nombre = request.POST.get('lugar_nombre')
            lugar_direccion = request.POST.get('lugar_direccion')
            lugar_departamento = request.POST.get('lugar_departamento')
            lugar_latitud = request.POST.get('lugar_latitud')
            lugar_longitud = request.POST.get('lugar_longitud')
            
            lugar = Lugar.objects.create(
                nombre=lugar_nombre,
                direccion=lugar_direccion,
                departamento=lugar_departamento,
                latitud = float(request.POST.get('lugar_latitud', '0').replace(',', '.')),
                longitud = float(request.POST.get('lugar_longitud', '0').replace(',', '.'))
            )
            
            # Procesar datos del evento
            titulo = request.POST.get('titulo')
            descripcion = request.POST.get('descripcion')
            fecha_inicio = request.POST.get('fecha_inicio')
            fecha_fin = request.POST.get('fecha_fin')
            capacidad = request.POST.get('capacidad')
            modalidad = request.POST.get('modalidad')
            tipo_publico = request.POST.get('tipo_publico')
            
            evento = Evento.objects.create(
                titulo=titulo,
                descripcion=descripcion,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                capacidad=capacidad,
                modalidad=modalidad,
                categoria=CategoriaEvento.CULTURAL,
                tipo_publico=tipo_publico,
                lugar=lugar,
                usuario_creador=request.user
            )
            
            # Procesar imagen principal si existe
            if 'imagen_principal' in request.FILES:
                evento.imagen_principal = request.FILES['imagen_principal']
                evento.save()
            
            # Procesar patrocinadores si existen
            patrocinadores_ids = request.POST.getlist('patrocinadores')
            for patrocinador_id in patrocinadores_ids:
                patrocinador = Patrocinador.objects.get(id=patrocinador_id)
                evento.patrocinadores.add(patrocinador)
            
            # Procesar recursos si existen
            recursos_descripciones = request.POST.getlist('recursos_descripcion')
            recursos_tipos = request.POST.getlist('recursos_tipo')
            
            for descripcion, tipo in zip(recursos_descripciones, recursos_tipos):
                if descripcion:  # Solo crear si hay descripción
                    recurso = Recurso.objects.create(
                        tipo=tipo,
                        descripcion=descripcion
                    )
                    evento.recursos.add(recurso)
            
            # Procesar imágenes adicionales si existen
            imagenes = request.FILES.getlist('imagenes_evento')
            for imagen in imagenes:
                ImagenEvento.objects.create(
                    evento=evento,
                    imagen=imagen,
                    descripcion=f"Imagen de {evento.titulo}"
                )
            
            messages.success(request, 'Evento cultural creado exitosamente!')
            return redirect('culturalescrud')
        
        except Exception as e:
            print(e)
            messages.error(request, f'Error al crear el evento: {str(e)}')
            return redirect('crear_evento_cultural')
    
    # GET request - mostrar formulario
    patrocinadores = Patrocinador.objects.all()
    context = {
        'modalidades': ModalidadEvento.choices,
        'tipos_publico': TipoPublico.choices,
        'departamentos': DepartamentoBolivia.choices,
        'patrocinadores': patrocinadores
    }
    return render(request, 'crear_evento_cultural.html', context)

@login_required(login_url='index')
def editar_evento_cultural(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id, usuario_creador=request.user)
    
    if request.method == 'POST':
        try:
            # Actualizar datos del lugar
            lugar = evento.lugar
            lugar.nombre = request.POST.get('lugar_nombre')
            lugar.direccion = request.POST.get('lugar_direccion')
            lugar.departamento = request.POST.get('lugar_departamento')
            lugar.latitud = float(request.POST.get('lugar_latitud', '0').replace(',', '.'))
            lugar.longitud = float(request.POST.get('lugar_longitud', '0').replace(',', '.'))
            lugar.save()
            
            # Actualizar datos del evento
            evento.titulo = request.POST.get('titulo')
            evento.descripcion = request.POST.get('descripcion')
            evento.fecha_inicio = request.POST.get('fecha_inicio')
            evento.fecha_fin = request.POST.get('fecha_fin')
            evento.capacidad = request.POST.get('capacidad')
            evento.modalidad = request.POST.get('modalidad')
            evento.tipo_publico = request.POST.get('tipo_publico')
            
            # Actualizar imagen principal si se proporciona una nueva
            if 'imagen_principal' in request.FILES:
                evento.imagen_principal = request.FILES['imagen_principal']
            
            evento.save()
            
            # Actualizar patrocinadores
            evento.patrocinadores.clear()
            patrocinadores_ids = request.POST.getlist('patrocinadores')
            for patrocinador_id in patrocinadores_ids:
                patrocinador = Patrocinador.objects.get(id=patrocinador_id)
                evento.patrocinadores.add(patrocinador)
            
            # Actualizar recursos (eliminamos los existentes y creamos nuevos)
            evento.recursos.all().delete()
            recursos_descripciones = request.POST.getlist('recursos_descripcion',[])
            recursos_tipos = request.POST.getlist('recursos_tipo',[])
            print(recursos_descripciones)
            print(recursos_tipos)
            
            for descripcion, tipo in zip(recursos_descripciones, recursos_tipos):
                if descripcion:
                    recurso = Recurso.objects.create(
                        tipo=tipo,
                        descripcion=descripcion
                    )
                    evento.recursos.add(recurso)
            
            # Agregar nuevas imágenes si se proporcionan
            imagenes = request.FILES.getlist('imagenes_evento')
            for imagen in imagenes:
                ImagenEvento.objects.create(
                    evento=evento,
                    imagen=imagen,
                    descripcion=f"Imagen de {evento.titulo}"
                )
            
            messages.success(request, 'Evento cultural actualizado exitosamente!')
            return redirect('culturalescrud')
        
        except Exception as e:
            print(e)
            messages.error(request, f'Error al actualizar el evento: {str(e)}')
            return redirect('editar_evento_cultural', evento_id=evento_id)
    
    # GET request - mostrar formulario de edición
    patrocinadores = Patrocinador.objects.all()
    recursos = evento.recursos.all()
    imagenes = evento.imagenes.all()
    
    context = {
        'evento': evento,
        'lugar': evento.lugar,
        'modalidades': ModalidadEvento.choices,
        'tipos_publico': TipoPublico.choices,
        'departamentos': DepartamentoBolivia.choices,
        'patrocinadores': patrocinadores,
        'recursos': recursos,
        'imagenes': imagenes,
        'patrocinadores_seleccionados': [p.id for p in evento.patrocinadores.all()]
    }
    return render(request, 'editar_evento_cultural.html', context)

@login_required(login_url='index')
def eliminar_evento_cultural(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id, usuario_creador=request.user)
    
    if request.method == 'POST':
        try:
            # Eliminar el lugar asociado si no está siendo usado por otros eventos
            lugar = evento.lugar
            evento.delete()
            if lugar.eventos.count() == 0:
                lugar.delete()
            
            messages.success(request, 'Evento cultural eliminado exitosamente!')
        except Exception as e:
            messages.error(request, f'Error al eliminar el evento: {str(e)}')
        
        return redirect('culturalescrud')
    
    return render(request, 'eliminar_evento_cultural.html', {'evento': evento})

@login_required(login_url='index')
def eliminar_imagen_evento_cultural(request, imagen_id):
    imagen = get_object_or_404(ImagenEvento, id=imagen_id, evento__usuario_creador=request.user)
    evento_id = imagen.evento.id
    imagen.delete()
    messages.success(request, 'Imagen eliminada exitosamente!')
    return redirect('editar_evento_cultural', evento_id=evento_id)

@login_required(login_url='index')
def ver_evento_cultural(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id, usuario_creador=request.user)
    
    context = {
        'evento': evento,
        'lugar': evento.lugar,
        'patrocinadores': evento.patrocinadores.all(),
        'recursos': evento.recursos.all(),
        'imagenes': evento.imagenes.all()
    }
    return render(request, 'ver_evento_cultural.html', context)







@login_required(login_url='index')
def gastronomicoscrud(request):
    # Listar todos los eventos académicos
    eventos = Evento.objects.filter(categoria=CategoriaEvento.GASTRONOMICO, usuario_creador=request.user)
    return render(request, 'gastronomicoscrud.html', {'eventos': eventos})

@login_required(login_url='index')
def crear_evento_gastronomico(request):
    if request.method == 'POST':
        try:
            # Procesar datos del lugar
            lugar_nombre = request.POST.get('lugar_nombre')
            lugar_direccion = request.POST.get('lugar_direccion')
            lugar_departamento = request.POST.get('lugar_departamento')
            lugar_latitud = request.POST.get('lugar_latitud')
            lugar_longitud = request.POST.get('lugar_longitud')
            
            lugar = Lugar.objects.create(
                nombre=lugar_nombre,
                direccion=lugar_direccion,
                departamento=lugar_departamento,
                latitud = float(request.POST.get('lugar_latitud', '0').replace(',', '.')),
                longitud = float(request.POST.get('lugar_longitud', '0').replace(',', '.'))
            )
            
            # Procesar datos del evento
            titulo = request.POST.get('titulo')
            descripcion = request.POST.get('descripcion')
            fecha_inicio = request.POST.get('fecha_inicio')
            fecha_fin = request.POST.get('fecha_fin')
            capacidad = request.POST.get('capacidad')
            modalidad = request.POST.get('modalidad')
            tipo_publico = request.POST.get('tipo_publico')
            
            evento = Evento.objects.create(
                titulo=titulo,
                descripcion=descripcion,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                capacidad=capacidad,
                modalidad=modalidad,
                categoria=CategoriaEvento.GASTRONOMICO,
                tipo_publico=tipo_publico,
                lugar=lugar,
                usuario_creador=request.user
            )
            
            # Procesar imagen principal si existe
            if 'imagen_principal' in request.FILES:
                evento.imagen_principal = request.FILES['imagen_principal']
                evento.save()
            
            # Procesar patrocinadores si existen
            patrocinadores_ids = request.POST.getlist('patrocinadores')
            for patrocinador_id in patrocinadores_ids:
                patrocinador = Patrocinador.objects.get(id=patrocinador_id)
                evento.patrocinadores.add(patrocinador)
            
            # Procesar recursos si existen
            recursos_descripciones = request.POST.getlist('recursos_descripcion')
            recursos_tipos = request.POST.getlist('recursos_tipo')
            
            for descripcion, tipo in zip(recursos_descripciones, recursos_tipos):
                if descripcion:  # Solo crear si hay descripción
                    recurso = Recurso.objects.create(
                        tipo=tipo,
                        descripcion=descripcion
                    )
                    evento.recursos.add(recurso)
            
            # Procesar imágenes adicionales si existen
            imagenes = request.FILES.getlist('imagenes_evento')
            for imagen in imagenes:
                ImagenEvento.objects.create(
                    evento=evento,
                    imagen=imagen,
                    descripcion=f"Imagen de {evento.titulo}"
                )
            
            messages.success(request, 'Evento gastronomico creado exitosamente!')
            return redirect('gastronomicoscrud')
        
        except Exception as e:
            print(e)
            messages.error(request, f'Error al crear el evento: {str(e)}')
            return redirect('crear_evento_gastronomico')
    
    # GET request - mostrar formulario
    patrocinadores = Patrocinador.objects.all()
    context = {
        'modalidades': ModalidadEvento.choices,
        'tipos_publico': TipoPublico.choices,
        'departamentos': DepartamentoBolivia.choices,
        'patrocinadores': patrocinadores
    }
    return render(request, 'crear_evento_gastronomico.html', context)

@login_required(login_url='index')
def editar_evento_gastronomico(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id, usuario_creador=request.user)
    
    if request.method == 'POST':
        try:
            # Actualizar datos del lugar
            lugar = evento.lugar
            lugar.nombre = request.POST.get('lugar_nombre')
            lugar.direccion = request.POST.get('lugar_direccion')
            lugar.departamento = request.POST.get('lugar_departamento')
            lugar.latitud = float(request.POST.get('lugar_latitud', '0').replace(',', '.'))
            lugar.longitud = float(request.POST.get('lugar_longitud', '0').replace(',', '.'))
            lugar.save()
            
            # Actualizar datos del evento
            evento.titulo = request.POST.get('titulo')
            evento.descripcion = request.POST.get('descripcion')
            evento.fecha_inicio = request.POST.get('fecha_inicio')
            evento.fecha_fin = request.POST.get('fecha_fin')
            evento.capacidad = request.POST.get('capacidad')
            evento.modalidad = request.POST.get('modalidad')
            evento.tipo_publico = request.POST.get('tipo_publico')
            
            # Actualizar imagen principal si se proporciona una nueva
            if 'imagen_principal' in request.FILES:
                evento.imagen_principal = request.FILES['imagen_principal']
            
            evento.save()
            
            # Actualizar patrocinadores
            evento.patrocinadores.clear()
            patrocinadores_ids = request.POST.getlist('patrocinadores')
            for patrocinador_id in patrocinadores_ids:
                patrocinador = Patrocinador.objects.get(id=patrocinador_id)
                evento.patrocinadores.add(patrocinador)
            
            # Actualizar recursos (eliminamos los existentes y creamos nuevos)
            evento.recursos.all().delete()
            recursos_descripciones = request.POST.getlist('recursos_descripcion',[])
            recursos_tipos = request.POST.getlist('recursos_tipo',[])
            print(recursos_descripciones)
            print(recursos_tipos)
            
            for descripcion, tipo in zip(recursos_descripciones, recursos_tipos):
                if descripcion:
                    recurso = Recurso.objects.create(
                        tipo=tipo,
                        descripcion=descripcion
                    )
                    evento.recursos.add(recurso)
            
            # Agregar nuevas imágenes si se proporcionan
            imagenes = request.FILES.getlist('imagenes_evento')
            for imagen in imagenes:
                ImagenEvento.objects.create(
                    evento=evento,
                    imagen=imagen,
                    descripcion=f"Imagen de {evento.titulo}"
                )
            
            messages.success(request, 'Evento gastronomico actualizado exitosamente!')
            return redirect('gastronomicoscrud')
        
        except Exception as e:
            print(e)
            messages.error(request, f'Error al actualizar el evento: {str(e)}')
            return redirect('editar_evento_gastronomico', evento_id=evento_id)
    
    # GET request - mostrar formulario de edición
    patrocinadores = Patrocinador.objects.all()
    recursos = evento.recursos.all()
    imagenes = evento.imagenes.all()
    
    context = {
        'evento': evento,
        'lugar': evento.lugar,
        'modalidades': ModalidadEvento.choices,
        'tipos_publico': TipoPublico.choices,
        'departamentos': DepartamentoBolivia.choices,
        'patrocinadores': patrocinadores,
        'recursos': recursos,
        'imagenes': imagenes,
        'patrocinadores_seleccionados': [p.id for p in evento.patrocinadores.all()]
    }
    return render(request, 'editar_evento_gastronomico.html', context)

@login_required(login_url='index')
def eliminar_evento_gastronomico(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id, usuario_creador=request.user)
    
    if request.method == 'POST':
        try:
            # Eliminar el lugar asociado si no está siendo usado por otros eventos
            lugar = evento.lugar
            evento.delete()
            if lugar.eventos.count() == 0:
                lugar.delete()
            
            messages.success(request, 'Evento gastronomico eliminado exitosamente!')
        except Exception as e:
            messages.error(request, f'Error al eliminar el evento: {str(e)}')
        
        return redirect('gastronomicoscrud')
    
    return render(request, 'eliminar_evento_gastronomico.html', {'evento': evento})

@login_required(login_url='index')
def eliminar_imagen_evento_gastronomico(request, imagen_id):
    imagen = get_object_or_404(ImagenEvento, id=imagen_id, evento__usuario_creador=request.user)
    evento_id = imagen.evento.id
    imagen.delete()
    messages.success(request, 'Imagen eliminada exitosamente!')
    return redirect('editar_evento_gastronomico', evento_id=evento_id)

@login_required(login_url='index')
def ver_evento_gastronomico(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id, usuario_creador=request.user)
    
    context = {
        'evento': evento,
        'lugar': evento.lugar,
        'patrocinadores': evento.patrocinadores.all(),
        'recursos': evento.recursos.all(),
        'imagenes': evento.imagenes.all()
    }
    return render(request, 'ver_evento_gastronomico.html', context)









@login_required(login_url='index')
def deportivoscrud(request):
    # Listar todos los eventos académicos
    eventos = Evento.objects.filter(categoria=CategoriaEvento.DEPORTIVO, usuario_creador=request.user)
    return render(request, 'deportivoscrud.html', {'eventos': eventos})

@login_required(login_url='index')
def crear_evento_deportivo(request):
    if request.method == 'POST':
        try:
            # Procesar datos del lugar
            lugar_nombre = request.POST.get('lugar_nombre')
            lugar_direccion = request.POST.get('lugar_direccion')
            lugar_departamento = request.POST.get('lugar_departamento')
            lugar_latitud = request.POST.get('lugar_latitud')
            lugar_longitud = request.POST.get('lugar_longitud')
            
            lugar = Lugar.objects.create(
                nombre=lugar_nombre,
                direccion=lugar_direccion,
                departamento=lugar_departamento,
                latitud = float(request.POST.get('lugar_latitud', '0').replace(',', '.')),
                longitud = float(request.POST.get('lugar_longitud', '0').replace(',', '.'))
            )
            
            # Procesar datos del evento
            titulo = request.POST.get('titulo')
            descripcion = request.POST.get('descripcion')
            fecha_inicio = request.POST.get('fecha_inicio')
            fecha_fin = request.POST.get('fecha_fin')
            capacidad = request.POST.get('capacidad')
            modalidad = request.POST.get('modalidad')
            tipo_publico = request.POST.get('tipo_publico')
            
            evento = Evento.objects.create(
                titulo=titulo,
                descripcion=descripcion,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                capacidad=capacidad,
                modalidad=modalidad,
                categoria=CategoriaEvento.DEPORTIVO,
                tipo_publico=tipo_publico,
                lugar=lugar,
                usuario_creador=request.user
            )
            
            # Procesar imagen principal si existe
            if 'imagen_principal' in request.FILES:
                evento.imagen_principal = request.FILES['imagen_principal']
                evento.save()
            
            # Procesar patrocinadores si existen
            patrocinadores_ids = request.POST.getlist('patrocinadores')
            for patrocinador_id in patrocinadores_ids:
                patrocinador = Patrocinador.objects.get(id=patrocinador_id)
                evento.patrocinadores.add(patrocinador)
            
            # Procesar recursos si existen
            recursos_descripciones = request.POST.getlist('recursos_descripcion')
            recursos_tipos = request.POST.getlist('recursos_tipo')
            
            for descripcion, tipo in zip(recursos_descripciones, recursos_tipos):
                if descripcion:  # Solo crear si hay descripción
                    recurso = Recurso.objects.create(
                        tipo=tipo,
                        descripcion=descripcion
                    )
                    evento.recursos.add(recurso)
            
            # Procesar imágenes adicionales si existen
            imagenes = request.FILES.getlist('imagenes_evento')
            for imagen in imagenes:
                ImagenEvento.objects.create(
                    evento=evento,
                    imagen=imagen,
                    descripcion=f"Imagen de {evento.titulo}"
                )
            
            messages.success(request, 'Evento deportivo creado exitosamente!')
            return redirect('deportivoscrud')
        
        except Exception as e:
            print(e)
            messages.error(request, f'Error al crear el evento: {str(e)}')
            return redirect('crear_evento_deportivo')
    
    # GET request - mostrar formulario
    patrocinadores = Patrocinador.objects.all()
    context = {
        'modalidades': ModalidadEvento.choices,
        'tipos_publico': TipoPublico.choices,
        'departamentos': DepartamentoBolivia.choices,
        'patrocinadores': patrocinadores
    }
    return render(request, 'crear_evento_deportivo.html', context)

@login_required(login_url='index')
def editar_evento_deportivo(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id, usuario_creador=request.user)
    
    if request.method == 'POST':
        try:
            # Actualizar datos del lugar
            lugar = evento.lugar
            lugar.nombre = request.POST.get('lugar_nombre')
            lugar.direccion = request.POST.get('lugar_direccion')
            lugar.departamento = request.POST.get('lugar_departamento')
            lugar.latitud = float(request.POST.get('lugar_latitud', '0').replace(',', '.'))
            lugar.longitud = float(request.POST.get('lugar_longitud', '0').replace(',', '.'))
            lugar.save()
            
            # Actualizar datos del evento
            evento.titulo = request.POST.get('titulo')
            evento.descripcion = request.POST.get('descripcion')
            evento.fecha_inicio = request.POST.get('fecha_inicio')
            evento.fecha_fin = request.POST.get('fecha_fin')
            evento.capacidad = request.POST.get('capacidad')
            evento.modalidad = request.POST.get('modalidad')
            evento.tipo_publico = request.POST.get('tipo_publico')
            
            # Actualizar imagen principal si se proporciona una nueva
            if 'imagen_principal' in request.FILES:
                evento.imagen_principal = request.FILES['imagen_principal']
            
            evento.save()
            
            # Actualizar patrocinadores
            evento.patrocinadores.clear()
            patrocinadores_ids = request.POST.getlist('patrocinadores')
            for patrocinador_id in patrocinadores_ids:
                patrocinador = Patrocinador.objects.get(id=patrocinador_id)
                evento.patrocinadores.add(patrocinador)
            
            # Actualizar recursos (eliminamos los existentes y creamos nuevos)
            evento.recursos.all().delete()
            recursos_descripciones = request.POST.getlist('recursos_descripcion',[])
            recursos_tipos = request.POST.getlist('recursos_tipo',[])
            print(recursos_descripciones)
            print(recursos_tipos)
            
            for descripcion, tipo in zip(recursos_descripciones, recursos_tipos):
                if descripcion:
                    recurso = Recurso.objects.create(
                        tipo=tipo,
                        descripcion=descripcion
                    )
                    evento.recursos.add(recurso)
            
            # Agregar nuevas imágenes si se proporcionan
            imagenes = request.FILES.getlist('imagenes_evento')
            for imagen in imagenes:
                ImagenEvento.objects.create(
                    evento=evento,
                    imagen=imagen,
                    descripcion=f"Imagen de {evento.titulo}"
                )
            
            messages.success(request, 'Evento deportivo actualizado exitosamente!')
            return redirect('deportivoscrud')
        
        except Exception as e:
            print(e)
            messages.error(request, f'Error al actualizar el evento: {str(e)}')
            return redirect('editar_evento_deportivo', evento_id=evento_id)
    
    # GET request - mostrar formulario de edición
    patrocinadores = Patrocinador.objects.all()
    recursos = evento.recursos.all()
    imagenes = evento.imagenes.all()
    
    context = {
        'evento': evento,
        'lugar': evento.lugar,
        'modalidades': ModalidadEvento.choices,
        'tipos_publico': TipoPublico.choices,
        'departamentos': DepartamentoBolivia.choices,
        'patrocinadores': patrocinadores,
        'recursos': recursos,
        'imagenes': imagenes,
        'patrocinadores_seleccionados': [p.id for p in evento.patrocinadores.all()]
    }
    return render(request, 'editar_evento_deportivo.html', context)

@login_required(login_url='index')
def eliminar_evento_deportivo(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id, usuario_creador=request.user)
    
    if request.method == 'POST':
        try:
            # Eliminar el lugar asociado si no está siendo usado por otros eventos
            lugar = evento.lugar
            evento.delete()
            if lugar.eventos.count() == 0:
                lugar.delete()
            
            messages.success(request, 'Evento deportivo eliminado exitosamente!')
        except Exception as e:
            messages.error(request, f'Error al eliminar el evento: {str(e)}')
        
        return redirect('deportivoscrud')
    
    return render(request, 'eliminar_evento_deportivo.html', {'evento': evento})

@login_required(login_url='index')
def eliminar_imagen_evento_deportivo(request, imagen_id):
    imagen = get_object_or_404(ImagenEvento, id=imagen_id, evento__usuario_creador=request.user)
    evento_id = imagen.evento.id
    imagen.delete()
    messages.success(request, 'Imagen eliminada exitosamente!')
    return redirect('editar_evento_deportivo', evento_id=evento_id)

@login_required(login_url='index')
def ver_evento_deportivo(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id, usuario_creador=request.user)
    
    context = {
        'evento': evento,
        'lugar': evento.lugar,
        'patrocinadores': evento.patrocinadores.all(),
        'recursos': evento.recursos.all(),
        'imagenes': evento.imagenes.all()
    }
    return render(request, 'ver_evento_deportivo.html', context)








@login_required(login_url='index')
def feriacrud(request):
    # Listar todos los eventos académicos
    eventos = Evento.objects.filter(categoria=CategoriaEvento.FERIA, usuario_creador=request.user)
    return render(request, 'feriacrud.html', {'eventos': eventos})

@login_required(login_url='index')
def crear_evento_feria(request):
    if request.method == 'POST':
        try:
            # Procesar datos del lugar
            lugar_nombre = request.POST.get('lugar_nombre')
            lugar_direccion = request.POST.get('lugar_direccion')
            lugar_departamento = request.POST.get('lugar_departamento')
            lugar_latitud = request.POST.get('lugar_latitud')
            lugar_longitud = request.POST.get('lugar_longitud')
            
            lugar = Lugar.objects.create(
                nombre=lugar_nombre,
                direccion=lugar_direccion,
                departamento=lugar_departamento,
                latitud = float(request.POST.get('lugar_latitud', '0').replace(',', '.')),
                longitud = float(request.POST.get('lugar_longitud', '0').replace(',', '.'))
            )
            
            # Procesar datos del evento
            titulo = request.POST.get('titulo')
            descripcion = request.POST.get('descripcion')
            fecha_inicio = request.POST.get('fecha_inicio')
            fecha_fin = request.POST.get('fecha_fin')
            capacidad = request.POST.get('capacidad')
            modalidad = request.POST.get('modalidad')
            tipo_publico = request.POST.get('tipo_publico')
            
            evento = Evento.objects.create(
                titulo=titulo,
                descripcion=descripcion,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                capacidad=capacidad,
                modalidad=modalidad,
                categoria=CategoriaEvento.FERIA,
                tipo_publico=tipo_publico,
                lugar=lugar,
                usuario_creador=request.user
            )
            
            # Procesar imagen principal si existe
            if 'imagen_principal' in request.FILES:
                evento.imagen_principal = request.FILES['imagen_principal']
                evento.save()
            
            # Procesar patrocinadores si existen
            patrocinadores_ids = request.POST.getlist('patrocinadores')
            for patrocinador_id in patrocinadores_ids:
                patrocinador = Patrocinador.objects.get(id=patrocinador_id)
                evento.patrocinadores.add(patrocinador)
            
            # Procesar recursos si existen
            recursos_descripciones = request.POST.getlist('recursos_descripcion')
            recursos_tipos = request.POST.getlist('recursos_tipo')
            
            for descripcion, tipo in zip(recursos_descripciones, recursos_tipos):
                if descripcion:  # Solo crear si hay descripción
                    recurso = Recurso.objects.create(
                        tipo=tipo,
                        descripcion=descripcion
                    )
                    evento.recursos.add(recurso)
            
            # Procesar imágenes adicionales si existen
            imagenes = request.FILES.getlist('imagenes_evento')
            for imagen in imagenes:
                ImagenEvento.objects.create(
                    evento=evento,
                    imagen=imagen,
                    descripcion=f"Imagen de {evento.titulo}"
                )
            
            messages.success(request, 'Evento feria creado exitosamente!')
            return redirect('feriacrud')
        
        except Exception as e:
            print(e)
            messages.error(request, f'Error al crear el evento: {str(e)}')
            return redirect('crear_evento_feria')
    
    # GET request - mostrar formulario
    patrocinadores = Patrocinador.objects.all()
    context = {
        'modalidades': ModalidadEvento.choices,
        'tipos_publico': TipoPublico.choices,
        'departamentos': DepartamentoBolivia.choices,
        'patrocinadores': patrocinadores
    }
    return render(request, 'crear_evento_feria.html', context)

@login_required(login_url='index')
def editar_evento_feria(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id, usuario_creador=request.user)
    
    if request.method == 'POST':
        try:
            # Actualizar datos del lugar
            lugar = evento.lugar
            lugar.nombre = request.POST.get('lugar_nombre')
            lugar.direccion = request.POST.get('lugar_direccion')
            lugar.departamento = request.POST.get('lugar_departamento')
            lugar.latitud = float(request.POST.get('lugar_latitud', '0').replace(',', '.'))
            lugar.longitud = float(request.POST.get('lugar_longitud', '0').replace(',', '.'))
            lugar.save()
            
            # Actualizar datos del evento
            evento.titulo = request.POST.get('titulo')
            evento.descripcion = request.POST.get('descripcion')
            evento.fecha_inicio = request.POST.get('fecha_inicio')
            evento.fecha_fin = request.POST.get('fecha_fin')
            evento.capacidad = request.POST.get('capacidad')
            evento.modalidad = request.POST.get('modalidad')
            evento.tipo_publico = request.POST.get('tipo_publico')
            
            # Actualizar imagen principal si se proporciona una nueva
            if 'imagen_principal' in request.FILES:
                evento.imagen_principal = request.FILES['imagen_principal']
            
            evento.save()
            
            # Actualizar patrocinadores
            evento.patrocinadores.clear()
            patrocinadores_ids = request.POST.getlist('patrocinadores')
            for patrocinador_id in patrocinadores_ids:
                patrocinador = Patrocinador.objects.get(id=patrocinador_id)
                evento.patrocinadores.add(patrocinador)
            
            # Actualizar recursos (eliminamos los existentes y creamos nuevos)
            evento.recursos.all().delete()
            recursos_descripciones = request.POST.getlist('recursos_descripcion',[])
            recursos_tipos = request.POST.getlist('recursos_tipo',[])
            print(recursos_descripciones)
            print(recursos_tipos)
            
            for descripcion, tipo in zip(recursos_descripciones, recursos_tipos):
                if descripcion:
                    recurso = Recurso.objects.create(
                        tipo=tipo,
                        descripcion=descripcion
                    )
                    evento.recursos.add(recurso)
            
            # Agregar nuevas imágenes si se proporcionan
            imagenes = request.FILES.getlist('imagenes_evento')
            for imagen in imagenes:
                ImagenEvento.objects.create(
                    evento=evento,
                    imagen=imagen,
                    descripcion=f"Imagen de {evento.titulo}"
                )
            
            messages.success(request, 'Evento feria actualizado exitosamente!')
            return redirect('feriacrud')
        
        except Exception as e:
            print(e)
            messages.error(request, f'Error al actualizar el evento: {str(e)}')
            return redirect('editar_evento_feria', evento_id=evento_id)
    
    # GET request - mostrar formulario de edición
    patrocinadores = Patrocinador.objects.all()
    recursos = evento.recursos.all()
    imagenes = evento.imagenes.all()
    
    context = {
        'evento': evento,
        'lugar': evento.lugar,
        'modalidades': ModalidadEvento.choices,
        'tipos_publico': TipoPublico.choices,
        'departamentos': DepartamentoBolivia.choices,
        'patrocinadores': patrocinadores,
        'recursos': recursos,
        'imagenes': imagenes,
        'patrocinadores_seleccionados': [p.id for p in evento.patrocinadores.all()]
    }
    return render(request, 'editar_evento_feria.html', context)

@login_required(login_url='index')
def eliminar_evento_feria(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id, usuario_creador=request.user)
    
    if request.method == 'POST':
        try:
            # Eliminar el lugar asociado si no está siendo usado por otros eventos
            lugar = evento.lugar
            evento.delete()
            if lugar.eventos.count() == 0:
                lugar.delete()
            
            messages.success(request, 'Evento feria eliminado exitosamente!')
        except Exception as e:
            messages.error(request, f'Error al eliminar el evento: {str(e)}')
        
        return redirect('feriacrud')
    
    return render(request, 'eliminar_evento_feria.html', {'evento': evento})

@login_required(login_url='index')
def eliminar_imagen_evento_feria(request, imagen_id):
    imagen = get_object_or_404(ImagenEvento, id=imagen_id, evento__usuario_creador=request.user)
    evento_id = imagen.evento.id
    imagen.delete()
    messages.success(request, 'Imagen eliminada exitosamente!')
    return redirect('editar_evento_feria', evento_id=evento_id)

@login_required(login_url='index')
def ver_evento_feria(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id, usuario_creador=request.user)
    
    context = {
        'evento': evento,
        'lugar': evento.lugar,
        'patrocinadores': evento.patrocinadores.all(),
        'recursos': evento.recursos.all(),
        'imagenes': evento.imagenes.all()
    }
    return render(request, 'ver_evento_feria.html', context)








@login_required(login_url='index')
def socialcrud(request):
    # Listar todos los eventos académicos
    eventos = Evento.objects.filter(categoria=CategoriaEvento.SOCIAL, usuario_creador=request.user)
    return render(request, 'socialcrud.html', {'eventos': eventos})

@login_required(login_url='index')
def crear_evento_social(request):
    if request.method == 'POST':
        try:
            # Procesar datos del lugar
            lugar_nombre = request.POST.get('lugar_nombre')
            lugar_direccion = request.POST.get('lugar_direccion')
            lugar_departamento = request.POST.get('lugar_departamento')
            lugar_latitud = request.POST.get('lugar_latitud')
            lugar_longitud = request.POST.get('lugar_longitud')
            
            lugar = Lugar.objects.create(
                nombre=lugar_nombre,
                direccion=lugar_direccion,
                departamento=lugar_departamento,
                latitud = float(request.POST.get('lugar_latitud', '0').replace(',', '.')),
                longitud = float(request.POST.get('lugar_longitud', '0').replace(',', '.'))
            )
            
            # Procesar datos del evento
            titulo = request.POST.get('titulo')
            descripcion = request.POST.get('descripcion')
            fecha_inicio = request.POST.get('fecha_inicio')
            fecha_fin = request.POST.get('fecha_fin')
            capacidad = request.POST.get('capacidad')
            modalidad = request.POST.get('modalidad')
            tipo_publico = request.POST.get('tipo_publico')
            
            evento = Evento.objects.create(
                titulo=titulo,
                descripcion=descripcion,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                capacidad=capacidad,
                modalidad=modalidad,
                categoria=CategoriaEvento.SOCIAL,
                tipo_publico=tipo_publico,
                lugar=lugar,
                usuario_creador=request.user
            )
            
            # Procesar imagen principal si existe
            if 'imagen_principal' in request.FILES:
                evento.imagen_principal = request.FILES['imagen_principal']
                evento.save()
            
            # Procesar patrocinadores si existen
            patrocinadores_ids = request.POST.getlist('patrocinadores')
            for patrocinador_id in patrocinadores_ids:
                patrocinador = Patrocinador.objects.get(id=patrocinador_id)
                evento.patrocinadores.add(patrocinador)
            
            # Procesar recursos si existen
            recursos_descripciones = request.POST.getlist('recursos_descripcion')
            recursos_tipos = request.POST.getlist('recursos_tipo')
            
            for descripcion, tipo in zip(recursos_descripciones, recursos_tipos):
                if descripcion:  # Solo crear si hay descripción
                    recurso = Recurso.objects.create(
                        tipo=tipo,
                        descripcion=descripcion
                    )
                    evento.recursos.add(recurso)
            
            # Procesar imágenes adicionales si existen
            imagenes = request.FILES.getlist('imagenes_evento')
            for imagen in imagenes:
                ImagenEvento.objects.create(
                    evento=evento,
                    imagen=imagen,
                    descripcion=f"Imagen de {evento.titulo}"
                )
            
            messages.success(request, 'Evento social creado exitosamente!')
            return redirect('socialcrud')
        
        except Exception as e:
            print(e)
            messages.error(request, f'Error al crear el evento: {str(e)}')
            return redirect('crear_evento_social')
    
    # GET request - mostrar formulario
    patrocinadores = Patrocinador.objects.all()
    context = {
        'modalidades': ModalidadEvento.choices,
        'tipos_publico': TipoPublico.choices,
        'departamentos': DepartamentoBolivia.choices,
        'patrocinadores': patrocinadores
    }
    return render(request, 'crear_evento_social.html', context)

@login_required(login_url='index')
def editar_evento_social(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id, usuario_creador=request.user)
    
    if request.method == 'POST':
        try:
            # Actualizar datos del lugar
            lugar = evento.lugar
            lugar.nombre = request.POST.get('lugar_nombre')
            lugar.direccion = request.POST.get('lugar_direccion')
            lugar.departamento = request.POST.get('lugar_departamento')
            lugar.latitud = float(request.POST.get('lugar_latitud', '0').replace(',', '.'))
            lugar.longitud = float(request.POST.get('lugar_longitud', '0').replace(',', '.'))
            lugar.save()
            
            # Actualizar datos del evento
            evento.titulo = request.POST.get('titulo')
            evento.descripcion = request.POST.get('descripcion')
            evento.fecha_inicio = request.POST.get('fecha_inicio')
            evento.fecha_fin = request.POST.get('fecha_fin')
            evento.capacidad = request.POST.get('capacidad')
            evento.modalidad = request.POST.get('modalidad')
            evento.tipo_publico = request.POST.get('tipo_publico')
            
            # Actualizar imagen principal si se proporciona una nueva
            if 'imagen_principal' in request.FILES:
                evento.imagen_principal = request.FILES['imagen_principal']
            
            evento.save()
            
            # Actualizar patrocinadores
            evento.patrocinadores.clear()
            patrocinadores_ids = request.POST.getlist('patrocinadores')
            for patrocinador_id in patrocinadores_ids:
                patrocinador = Patrocinador.objects.get(id=patrocinador_id)
                evento.patrocinadores.add(patrocinador)
            
            # Actualizar recursos (eliminamos los existentes y creamos nuevos)
            evento.recursos.all().delete()
            recursos_descripciones = request.POST.getlist('recursos_descripcion',[])
            recursos_tipos = request.POST.getlist('recursos_tipo',[])
            print(recursos_descripciones)
            print(recursos_tipos)
            
            for descripcion, tipo in zip(recursos_descripciones, recursos_tipos):
                if descripcion:
                    recurso = Recurso.objects.create(
                        tipo=tipo,
                        descripcion=descripcion
                    )
                    evento.recursos.add(recurso)
            
            # Agregar nuevas imágenes si se proporcionan
            imagenes = request.FILES.getlist('imagenes_evento')
            for imagen in imagenes:
                ImagenEvento.objects.create(
                    evento=evento,
                    imagen=imagen,
                    descripcion=f"Imagen de {evento.titulo}"
                )
            
            messages.success(request, 'Evento social actualizado exitosamente!')
            return redirect('socialcrud')
        
        except Exception as e:
            print(e)
            messages.error(request, f'Error al actualizar el evento: {str(e)}')
            return redirect('editar_evento_social', evento_id=evento_id)
    
    # GET request - mostrar formulario de edición
    patrocinadores = Patrocinador.objects.all()
    recursos = evento.recursos.all()
    imagenes = evento.imagenes.all()
    
    context = {
        'evento': evento,
        'lugar': evento.lugar,
        'modalidades': ModalidadEvento.choices,
        'tipos_publico': TipoPublico.choices,
        'departamentos': DepartamentoBolivia.choices,
        'patrocinadores': patrocinadores,
        'recursos': recursos,
        'imagenes': imagenes,
        'patrocinadores_seleccionados': [p.id for p in evento.patrocinadores.all()]
    }
    return render(request, 'editar_evento_social.html', context)

@login_required(login_url='index')
def eliminar_evento_social(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id, usuario_creador=request.user)
    
    if request.method == 'POST':
        try:
            # Eliminar el lugar asociado si no está siendo usado por otros eventos
            lugar = evento.lugar
            evento.delete()
            if lugar.eventos.count() == 0:
                lugar.delete()
            
            messages.success(request, 'Evento social eliminado exitosamente!')
        except Exception as e:
            messages.error(request, f'Error al eliminar el evento: {str(e)}')
        
        return redirect('socialcrud')
    
    return render(request, 'eliminar_evento_social.html', {'evento': evento})

@login_required(login_url='index')
def eliminar_imagen_evento_social(request, imagen_id):
    imagen = get_object_or_404(ImagenEvento, id=imagen_id, evento__usuario_creador=request.user)
    evento_id = imagen.evento.id
    imagen.delete()
    messages.success(request, 'Imagen eliminada exitosamente!')
    return redirect('editar_evento_social', evento_id=evento_id)

@login_required(login_url='index')
def ver_evento_social(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id, usuario_creador=request.user)
    
    context = {
        'evento': evento,
        'lugar': evento.lugar,
        'patrocinadores': evento.patrocinadores.all(),
        'recursos': evento.recursos.all(),
        'imagenes': evento.imagenes.all()
    }
    return render(request, 'ver_evento_social.html', context)




#register
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.contrib.auth.forms import UserCreationForm
from django_countries.fields import CountryField
from cities_light.models import Country, Region, City
from .models import Usuario
import json
from django.http import JsonResponse
from django_countries import countries
from django import forms
from django.contrib.auth.forms import UserCreationForm


def registro(request):
    if request.method == 'POST':
        # Obtener los datos del formulario directamente desde request.POST
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        genero = request.POST.get('genero')
        numero_telefono = request.POST.get('numero_telefono')
        pais = request.POST.get('pais')
        ciudad = request.POST.get('ciudad')

        # Validaciones
        if not first_name or not last_name or not username or not email or not password1 or not password2:
            messages.error(request, 'Por favor completa todos los campos.')
            return render(request, 'registro.html', {'countries': countries})

        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'registro.html', {'countries': countries})

        if len(password1) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
            return render(request, 'registro.html', {'countries': countries})

        # Validar si el correo ya está registrado
        if Usuario.objects.filter(email=email).exists():
            messages.error(request, 'Este correo electrónico ya está registrado.')
            return render(request, 'registro.html', {'countries': countries})

        # Validar si el nombre de usuario ya está en uso
        if Usuario.objects.filter(username=username).exists():
            messages.error(request, 'Este nombre de usuario ya está en uso.')
            return render(request, 'registro.html', {'countries': countries})

        # Si todo está bien, crear el usuario
        user = Usuario.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password1,
            genero=genero,
            numero_telefono=numero_telefono,
            pais=pais,
            ciudad=ciudad,
            email_confirmado=False,
            codigo_confirmacion=get_random_string(length=32)
        )

        # Enviar correo de confirmación
        subject = 'Confirma tu correo electrónico'
        message = f'Hola {user.first_name},\n\nPor favor confirma tu correo electrónico haciendo clic en el siguiente enlace:\n\n{settings.BASE_URL}/confirmar-email/{user.codigo_confirmacion}/\n\nGracias!'
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        messages.success(request, 'Por favor revisa tu correo electrónico para confirmar tu cuenta.')
        return redirect('login')
    
    return render(request, 'registro.html', {'countries': countries})

def confirmar_email(request, codigo):
    try:
        user = Usuario.objects.get(codigo_confirmacion=codigo)
        user.email_confirmado = True
        user.codigo_confirmacion = None
        user.save()
        messages.success(request, 'Tu correo electrónico ha sido confirmado. Ahora puedes iniciar sesión.')
    except Usuario.DoesNotExist:
        messages.error(request, 'Código de confirmación inválido.')
    return redirect('login')

def cargar_ciudades(request):
    country_code = request.GET.get('country')  # Código de país como 'BO', 'US', etc.
    
    if not country_code:
        return JsonResponse({'ciudades': []}, status=400)
    
    try:
        # Primero obtener el país por su código
        country = Country.objects.get(code2=country_code)
        
        # Luego obtener las ciudades de ese país
        cities = City.objects.filter(country_id=country.id).order_by('name')
        dep = Region.objects.filter(country_id=country.id).order_by('name')
        
        ciudades = [city.name for city in cities] + [depa.name for depa in dep]
        
        # Ordenar la lista combinada alfabéticamente
        ciudades.sort()
        return JsonResponse({'ciudades': ciudades})
    
    except Country.DoesNotExist:
        return JsonResponse({'ciudades': []}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    




from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import ollama
from datetime import date
def generar_prompt_para_ollama(mensaje_usuario):
    eventos = Evento.objects.filter(fecha_fin__gte=date.today())
    historias = Historia.objects.all()[:5]
    presidentes = Presidente.objects.all()[:5]
    noticias = Noticia.objects.order_by('-fecha_publicacion')[:5]

    eventos_texto = "\n".join([
        f"- {e.titulo or 'Título no disponible'} ({e.categoria or 'Categoría no disponible'}) en {e.lugar.nombre or 'Lugar no disponible'}, {e.lugar.departamento or 'Departamento no disponible'}, el {e.fecha_inicio.strftime('%d-%m-%Y') if e.fecha_inicio else 'Fecha no disponible'} [{e.modalidad or 'Modalidad no disponible'}]. Público objetivo: {e.tipo_publico or 'Público no disponible'}."
        for e in eventos
    ])

    historias_texto = "\n".join([
        f"- {h.nombre or 'Nombre no disponible'}: {h.descripcion[:100] or 'Descripción no disponible'}..." for h in historias
    ])

    presidentes_texto = "\n".join([
        f"- {p.nombre or 'Nombre no disponible'} ({p.mandato or 'Mandato no disponible'}), nacido en {p.lugar_nacimiento or 'Lugar de nacimiento no disponible'}. Partido: {p.partido or 'Partido no disponible'}." for p in presidentes
    ])

    noticias_texto = "\n".join([
        f"- {n.titulo or 'Título no disponible'} ({n.fecha_publicacion or 'Fecha no disponible'}): {n.contenido[:80] or 'Contenido no disponible'}..." for n in noticias
    ])

    prompt = f"""
Eres un asistente experto en historia, cultura, eventos y actualidad de Bolivia y bicentenario de Bolivia (solo responde cosas que tienen que ver con Bolivia). El usuario quiere hacer una consulta.

Eventos:
{eventos_texto or 'No hay eventos próximos registrados.'}

Historias:
{historias_texto or 'No hay historias registradas.'}

Presidentes:
{presidentes_texto or 'No hay presidentes registrados.'}

Noticias:
{noticias_texto or 'No hay noticias registradas.'}

Responde a la siguiente pregunta del usuario de forma clara, con base en los datos anteriores (sobre eventos, historias, presidentes y ultimas noticias o preguntas relacionadas a Bolivia):
{mensaje_usuario}
"""
    return prompt

@csrf_exempt  # Solo para pruebas; en producción, usa CSRF correctamente
def ollama_response(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            consulta = data.get("message", "")
            response = ollama.chat(
                model="llama3.2:1b",  # Usa el nombre correcto de tu modelo local
                messages=[{"role": "user", "content": generar_prompt_para_ollama(consulta)}],
                options={"temperature": 0.8}
            )

            respuesta = response["message"]["content"]
            return JsonResponse({"response": respuesta})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Método no permitido"}, status=405)