# Generated by Django 5.2 on 2025-05-02 16:52

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
import django_countries.fields
import pagina.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('cities_light', '0011_alter_city_country_alter_city_region_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsejoNacional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('cargo', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('foto', models.ImageField(upload_to='consejo_fotos/')),
            ],
        ),
        migrations.CreateModel(
            name='Convocatoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255)),
                ('descripcion', models.TextField()),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='convocatorias/')),
                ('archivo_pdf', models.FileField(blank=True, null=True, upload_to='convocatorias/pdfs/')),
                ('fecha_publicacion', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Expositor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('img', models.ImageField(blank=True, null=True, upload_to='expositores/')),
            ],
        ),
        migrations.CreateModel(
            name='Fuente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('referencia', models.TextField()),
                ('url', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Lugar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=255)),
                ('departamento', models.CharField(choices=[('Chuquisaca', 'Chuquisaca'), ('La Paz', 'La Paz'), ('Cochabamba', 'Cochabamba'), ('Oruro', 'Oruro'), ('Potosí', 'Potosí'), ('Tarija', 'Tarija'), ('Santa Cruz', 'Santa Cruz'), ('Beni', 'Beni'), ('Pando', 'Pando')], max_length=20)),
                ('latitud', models.FloatField()),
                ('longitud', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Multimedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo', models.FileField(upload_to='multimedia/')),
                ('tipo', models.CharField(choices=[('imagen', 'Imagen'), ('video', 'Video'), ('audio', 'Audio'), ('documento', 'Documento')], max_length=50)),
                ('descripcion', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Patrocinador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to=pagina.models.logo_patrocinador_path)),
            ],
        ),
        migrations.CreateModel(
            name='PatrocinadorPagina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to=pagina.models.logo_patrocinador_path)),
            ],
        ),
        migrations.CreateModel(
            name='Presentacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('descripcion', models.TextField()),
                ('archivo', models.ImageField(blank=True, null=True, upload_to='presentaciones/')),
            ],
        ),
        migrations.CreateModel(
            name='Recurso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('Material', 'Material'), ('Tecnológico', 'Tecnológico'), ('Humano', 'Humano')], max_length=20)),
                ('descripcion', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Correo Electrónico')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_nacimiento', models.DateField(blank=True, null=True)),
                ('genero', models.CharField(blank=True, choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro'), ('N', 'Prefiero no decir')], max_length=1, null=True)),
                ('numero_telefono', models.CharField(blank=True, max_length=20, null=True)),
                ('pais', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('es_eventos', models.BooleanField(default=False)),
                ('es_cultural', models.BooleanField(default=False)),
                ('es_sistema', models.BooleanField(default=False)),
                ('email_confirmado', models.BooleanField(default=False)),
                ('codigo_confirmacion', models.CharField(blank=True, max_length=100, null=True)),
                ('ciudad', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cities_light.city')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenido', models.TextField()),
                ('fecha_comentario', models.DateField()),
                ('archivo', models.ImageField(blank=True, null=True, upload_to='comentarios/')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('descripcion', models.TextField()),
                ('fecha_inicio', models.DateTimeField()),
                ('fecha_fin', models.DateTimeField()),
                ('capacidad', models.PositiveIntegerField()),
                ('modalidad', models.CharField(choices=[('Presencial', 'Presencial'), ('Virtual', 'Virtual'), ('Mixto', 'Mixto')], max_length=10)),
                ('categoria', models.CharField(choices=[('Cultural', 'Cultural'), ('Deportivo', 'Deportivo'), ('Gastronomico', 'Gastronomico'), ('Academico', 'Academico'), ('Feria', 'Feria'), ('Social', 'Social')], max_length=20)),
                ('tipo_publico', models.CharField(choices=[('Infantil', 'Infantil'), ('Juvenil', 'Juvenil'), ('Adulto', 'Adulto'), ('General', 'General')], max_length=10)),
                ('imagen_principal', models.ImageField(blank=True, null=True, upload_to=pagina.models.evento_imagen_principal_path)),
                ('usuario_creador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eventos_creados', to=settings.AUTH_USER_MODEL)),
                ('expositores', models.ManyToManyField(blank=True, related_name='eventos', to='pagina.expositor')),
                ('lugar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='eventos', to='pagina.lugar')),
                ('patrocinadores', models.ManyToManyField(blank=True, related_name='eventos', to='pagina.patrocinador')),
                ('recursos', models.ManyToManyField(blank=True, related_name='eventos', to='pagina.recurso')),
            ],
        ),
        migrations.CreateModel(
            name='Historia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('tipo', models.CharField(choices=[('batalla', 'Batalla'), ('independencia', 'Independencia'), ('personaje', 'Personaje'), ('otro', 'Otro')], default='otro', max_length=20)),
                ('descripcion', models.TextField()),
                ('fecha', models.DateField()),
                ('fuente', models.ManyToManyField(blank=True, related_name='fuentes', to='pagina.fuente')),
                ('multimedia', models.ManyToManyField(blank=True, related_name='historias', to='pagina.multimedia')),
            ],
        ),
        migrations.CreateModel(
            name='ImagenEvento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(upload_to=pagina.models.imagen_evento_path)),
                ('descripcion', models.CharField(blank=True, max_length=255)),
                ('evento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagenes', to='pagina.evento')),
            ],
        ),
        migrations.CreateModel(
            name='Independencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField(blank=True, null=True)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='independencias/')),
                ('descripcion', models.TextField()),
                ('historia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pagina.historia')),
            ],
        ),
        migrations.CreateModel(
            name='Etnia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('lenguaje', models.CharField(max_length=255)),
                ('costumbres', models.TextField()),
                ('fuente', models.ManyToManyField(blank=True, related_name='etnias', to='pagina.fuente')),
                ('multimedia', models.ManyToManyField(blank=True, related_name='etnias', to='pagina.multimedia')),
            ],
        ),
        migrations.CreateModel(
            name='ArteYArtesania',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('origen', models.CharField(max_length=255)),
                ('descripcion', models.TextField()),
                ('fuente', models.ManyToManyField(blank=True, related_name='artes_y_artesanias', to='pagina.fuente')),
                ('multimedia', models.ManyToManyField(blank=True, related_name='artes_y_artesanias', to='pagina.multimedia')),
            ],
        ),
        migrations.CreateModel(
            name='Museo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('descripcion', models.TextField()),
                ('fuente', models.ManyToManyField(blank=True, related_name='museos', to='pagina.fuente')),
                ('lugar', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pagina.lugar')),
                ('multimedia', models.ManyToManyField(blank=True, related_name='museos', to='pagina.multimedia')),
            ],
        ),
        migrations.CreateModel(
            name='Noticia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255)),
                ('contenido', models.TextField()),
                ('fecha_publicacion', models.DateField(auto_now_add=True)),
                ('autor', models.CharField(max_length=255)),
                ('multimedia', models.ManyToManyField(blank=True, related_name='noticias', to='pagina.multimedia')),
            ],
        ),
        migrations.CreateModel(
            name='Presidente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('fecha_nacimiento', models.DateField(blank=True, null=True)),
                ('lugar_nacimiento', models.CharField(max_length=255)),
                ('descripcion', models.TextField()),
                ('partido', models.CharField(max_length=255)),
                ('educacion', models.CharField(max_length=255)),
                ('profesion', models.CharField(max_length=255)),
                ('mandato', models.CharField(max_length=100)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='presidentes/')),
                ('historia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pagina.historia')),
            ],
        ),
        migrations.CreateModel(
            name='Turismo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('descripcion', models.TextField()),
                ('fuente', models.ManyToManyField(blank=True, related_name='turismo', to='pagina.fuente')),
                ('lugar', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pagina.lugar')),
                ('multimedia', models.ManyToManyField(blank=True, related_name='turismo', to='pagina.multimedia')),
            ],
        ),
    ]
