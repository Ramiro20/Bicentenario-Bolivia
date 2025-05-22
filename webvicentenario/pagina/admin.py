from django.contrib import admin
from .models import *


admin.site.register(Independencia)
admin.site.register(Presidente)
admin.site.register(Usuario)
admin.site.register(Comentario)
admin.site.register(Noticia)
admin.site.register(Presentacion)
admin.site.register(ConsejoNacional)
admin.site.register(Convocatoria)
admin.site.register(Expositor)
admin.site.register(EnlaceEvento)


# Admin para Historia
@admin.register(Historia)
class HistoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'fecha')
    list_filter = ('tipo', 'fecha')
    search_fields = ('nombre', 'descripcion')
    filter_horizontal = ('multimedia', 'fuente')
    autocomplete_fields = ['fuente']  # Si tienes relaciones de tipo autocomplete con fuentes, etc.
    
    fieldsets = (
        (None, {
            'fields': ('nombre', 'descripcion', 'fecha', 'tipo')
        }),
        ('Multimedia y Fuentes', {
            'fields': ('multimedia', 'fuente')
        }),
    )

# Admin para Fuente
@admin.register(Fuente)
class FuenteAdmin(admin.ModelAdmin):
    list_display = ('referencia', 'url')
    search_fields = ('referencia', 'url')

# Admin para Multimedia
@admin.register(Multimedia)
class MultimediaAdmin(admin.ModelAdmin):
    list_display = ('archivo', 'descripcion')
    search_fields = ('descripcion',)

# --- Inlines para imágenes del evento ---

class ImagenEventoInline(admin.TabularInline):  # o admin.StackedInline para más espacio
    model = ImagenEvento
    extra = 1  # Número de formularios vacíos por defecto
    fields = ('imagen', 'descripcion')
    verbose_name = "Imagen adicional"
    verbose_name_plural = "Imágenes del evento"

# --- Admin de Evento ---

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_inicio', 'fecha_fin', 'categoria', 'modalidad', 'tipo_publico', 'lugar')
    list_filter = ('categoria', 'modalidad', 'tipo_publico', 'lugar__departamento')
    search_fields = ('titulo', 'descripcion')
    inlines = [ImagenEventoInline]
    autocomplete_fields = ['lugar', 'patrocinadores', 'recursos']
    readonly_fields = ('imagen_principal_preview',)

    fieldsets = (
        (None, {
            'fields': ('titulo', 'descripcion', 'imagen_principal', 'imagen_principal_preview')
        }),
        ('Información del evento', {
            'fields': (
                'fecha_inicio', 'fecha_fin', 'capacidad',
                'modalidad', 'categoria', 'tipo_publico', 'lugar'
            )
        }),
        ('Relaciones', {
            'fields': ('patrocinadores', 'recursos')
        }),
        ('Usuario', {
            'fields': ('usuario_creador',)
        }),
    )

    def imagen_principal_preview(self, obj):
        if obj.imagen_principal:
            return f'<img src="{obj.imagen_principal.url}" width="200" style="object-fit:contain;" />'
        return "Sin imagen"
    imagen_principal_preview.allow_tags = True
    imagen_principal_preview.short_description = 'Vista previa de imagen principal'
# --- Admin de Lugar ---

@admin.register(Lugar)
class LugarAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'departamento', 'direccion')
    search_fields = ('nombre', 'direccion')

# --- Admin de Patrocinador ---

@admin.register(Patrocinador)
class PatrocinadorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'logo_preview')
    search_fields = ('nombre', 'descripcion')
    readonly_fields = ('logo_preview',)

    def logo_preview(self, obj):
        if obj.logo:
            return f'<img src="{obj.logo.url}" width="100" style="object-fit:contain;" />'
        return "Sin logo"
    logo_preview.allow_tags = True
    logo_preview.short_description = 'Vista previa de logo'

# --- Admin de Recurso ---
@admin.register(PatrocinadorPagina)
class PatrocinadorPaginaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'logo_preview')
    search_fields = ('nombre', 'descripcion')
    readonly_fields = ('logo_preview',)

    def logo_preview(self, obj):
        if obj.logo:
            return f'<img src="{obj.logo.url}" width="100" style="object-fit:contain;" />'
        return "Sin logo"
    logo_preview.allow_tags = True
    logo_preview.short_description = 'Vista previa de logo'

@admin.register(Recurso)
class RecursoAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'descripcion')
    search_fields = ('descripcion',)

@admin.register(Museo)
class MuseoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'lugar')
    list_filter = ('lugar__departamento',)
    filter_horizontal = ('multimedia', 'fuente')

@admin.register(Turismo)
class TurismoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'lugar')
    search_fields = ('nombre',)
    list_filter = ('lugar__departamento',)
    filter_horizontal = ('multimedia', 'fuente')

@admin.register(ArteYArtesania)
class ArteYArtesaniaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'origen')
    search_fields = ('nombre', 'origen')
    filter_horizontal = ('multimedia', 'fuente')

@admin.register(Etnia)
class EtniaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'lenguaje')
    search_fields = ('nombre', 'lenguaje')
    filter_horizontal = ('multimedia', 'fuente')