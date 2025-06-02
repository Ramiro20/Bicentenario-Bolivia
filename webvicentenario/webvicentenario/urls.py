"""
URL configuration for webvicentenario project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from pagina import views
from django.conf import settings

from django.views.static import serve
from django.contrib.auth import views as auth_views

urlpatterns = [
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('consejo/', views.consejo, name='consejo'),
    path('batallas/', views.batallas, name='batallas'),
    path('independencias/', views.independencias, name='independencias'),
    path('personajes/', views.personajes, name='personajes'),
    path('presidentes/', views.presidentes, name='presidentes'),
    path('museos/', views.museos, name='museos'),
    path('artes/', views.artes, name='artes'),
    path('turismo/', views.turismo, name='turismo'),
    path('etnias/', views.etnias, name='etnias'),
    path('academicos/', views.academicos, name='academicos'),
    path('culturales/', views.culturales, name='culturales'),
    path('gastronomicos/', views.gastronomicos, name='gastronomicos'),
    path('deportivos/', views.deportivos, name='deportivos'),
    path('feria/', views.feria, name='feria'),
    path('social/', views.social, name='social'),

    path('academicoscrud/', views.academicoscrud, name='academicoscrud'),
    path('academicoscrud/crear/', views.crear_evento_academico, name='crear_evento_academico'),
    path('academicoscrud/editar/<int:evento_id>/', views.editar_evento_academico, name='editar_evento_academico'),
    path('academicoscrud/eliminar/<int:evento_id>/', views.eliminar_evento_academico, name='eliminar_evento_academico'),
    path('academicoscrud/eliminar-imagen/<int:imagen_id>/', views.eliminar_imagen_evento, name='eliminar_imagen_evento'),
    path('academicoscrud/ver/<int:evento_id>/', views.ver_evento_academico, name='ver_evento_academico'),

    #rutas agregadas para consultas
    path('buscar_eventos/', views.buscar_eventos_por_fecha, name='buscar_eventos_por_fecha'),

    path('culturalescrud/', views.culturalescrud, name='culturalescrud'),
    path('culturalescrud/crear/', views.crear_evento_cultural, name='crear_evento_cultural'),
    path('culturalescrud/editar/<int:evento_id>/', views.editar_evento_cultural, name='editar_evento_cultural'),
    path('culturalescrud/eliminar/<int:evento_id>/', views.eliminar_evento_cultural, name='eliminar_evento_cultural'),
    path('culturalescrud/eliminar-imagen/<int:imagen_id>/', views.eliminar_imagen_evento_cultural, name='eliminar_imagen_evento_cultural'),
    path('culturalescrud/ver/<int:evento_id>/', views.ver_evento_cultural, name='ver_evento_cultural'),



    path('gastronomicoscrud/', views.gastronomicoscrud, name='gastronomicoscrud'),
    path('gastronomicoscrud/crear/', views.crear_evento_gastronomico, name='crear_evento_gastronomico'),
    path('gastronomicoscrud/editar/<int:evento_id>/', views.editar_evento_gastronomico, name='editar_evento_gastronomico'),
    path('gastronomicoscrud/eliminar/<int:evento_id>/', views.eliminar_evento_gastronomico, name='eliminar_evento_gastronomico'),
    path('gastronomicoscrud/eliminar-imagen/<int:imagen_id>/', views.eliminar_imagen_evento_gastronomico, name='eliminar_imagen_evento_gastronomico'),
    path('gastronomicoscrud/ver/<int:evento_id>/', views.ver_evento_gastronomico, name='ver_evento_gastronomico'),






    path('deportivoscrud/', views.deportivoscrud, name='deportivoscrud'),
    path('deportivoscrud/crear/', views.crear_evento_deportivo, name='crear_evento_deportivo'),
    path('deportivoscrud/editar/<int:evento_id>/', views.editar_evento_deportivo, name='editar_evento_deportivo'),
    path('deportivoscrud/eliminar/<int:evento_id>/', views.eliminar_evento_deportivo, name='eliminar_evento_deportivo'),
    path('deportivoscrud/eliminar-imagen/<int:imagen_id>/', views.eliminar_imagen_evento_deportivo, name='eliminar_imagen_evento_deportivo'),
    path('deportivoscrud/ver/<int:evento_id>/', views.ver_evento_deportivo, name='ver_evento_deportivo'),





    path('feriacrud/', views.feriacrud, name='feriacrud'),
    path('feriacrud/crear/', views.crear_evento_feria, name='crear_evento_feria'),
    path('feriacrud/editar/<int:evento_id>/', views.editar_evento_feria, name='editar_evento_feria'),
    path('feriacrud/eliminar/<int:evento_id>/', views.eliminar_evento_feria, name='eliminar_evento_feria'),
    path('feriacrud/eliminar-imagen/<int:imagen_id>/', views.eliminar_imagen_evento_feria, name='eliminar_imagen_evento_feria'),
    path('feriacrud/ver/<int:evento_id>/', views.ver_evento_feria, name='ver_evento_feria'),




    path('socialcrud/', views.socialcrud, name='socialcrud'),
    path('socialcrud/crear/', views.crear_evento_social, name='crear_evento_social'),
    path('socialcrud/editar/<int:evento_id>/', views.editar_evento_social, name='editar_evento_social'),
    path('socialcrud/eliminar/<int:evento_id>/', views.eliminar_evento_social, name='eliminar_evento_social'),
    path('socialcrud/eliminar-imagen/<int:imagen_id>/', views.eliminar_imagen_evento_social, name='eliminar_imagen_evento_social'),
    path('socialcrud/ver/<int:evento_id>/', views.ver_evento_social, name='ver_evento_social'),




    
    path('noticias/', views.noticias, name='noticias'),
    path('convocatorias/', views.convocatorias, name='convocatorias'),
    path('agenda/', views.agenda, name='agenda'),
    path('contactos/', views.contactos, name='contactos'),

    path('events/<int:evento_id>/', views.evento_detalle, name='evento_detalle'),
    path('login/', views.login, name='login'),
    path('refresh-captcha/', views.refresh_captcha, name='refresh_captcha'),
    path('captcha/', include('captcha.urls')),
    path('logout/', views.custom_logout, name='logout'),

    path('registro/', views.registro, name='registro'),
    path('confirmar-email/<str:codigo>/', views.confirmar_email, name='confirmar_email'),
    path('cargar-ciudades/', views.cargar_ciudades, name='cargar_ciudades'),




    path("chatbot/ollama-response/", views.ollama_response, name="ollama_response"),
]
