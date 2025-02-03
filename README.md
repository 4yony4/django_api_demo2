
# Guía para Crear un Servidor API REST en Debian usando Django

## 📌 Paso 1: Instalar dependencias necesarias

Antes de empezar, asegurémonos de que el sistema está actualizado. Ejecuta:

```bash
sudo apt update && sudo apt upgrade -y
```

Ahora instalamos Python3, el administrador de paquetes (pip) y el entorno virtual (venv):

```bash
sudo apt install python3 python3-venv python3-pip -y
```

## 📌 Paso 2: Crear un entorno virtual

Un entorno virtual es útil para aislar las dependencias del proyecto.

1️⃣ Creamos una carpeta para nuestro proyecto:

```bash
mkdir django_api_demo
cd django_api_demo
```

2️⃣ Creamos un entorno virtual dentro del proyecto:

```bash
python3 -m venv venv
```

3️⃣ Activamos el entorno virtual:

```bash
source venv/bin/activate
```

Ahora deberías ver algo así en tu terminal:
`(venv) usuario@debian:~/django_api_demo$`

## 📌 Paso 3: Instalar Django y Django REST Framework

Con el entorno virtual activado, instalamos Django y Django REST Framework:

```bash
pip install django djangorestframework
```

Verificamos que Django se instaló correctamente con:

```bash
django-admin --version
```

## 📌 Paso 4: Crear un proyecto Django

Ahora, creamos un proyecto llamado "apiserver" dentro de la carpeta:

```bash
django-admin startproject apiserver .
```

Esto generará varios archivos y una estructura como esta:

```
django_api_demo/
├── apiserver/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── manage.py
└── venv/
```

## 📌 Paso 5: Crear una aplicación dentro del proyecto

Django organiza el código en aplicaciones. Vamos a crear una app llamada "api":

```bash
python manage.py startapp api
```

Agregamos nuestra nueva aplicación y Django REST Framework a `apiserver/settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'api',
]
```

Aplicamos las migraciones iniciales:

```bash
python manage.py migrate
```

## 📌 Paso 6: Crear un modelo de datos

Editamos `api/models.py` y agregamos:

```python
from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
```

Aplicamos las migraciones:

```bash
python manage.py makemigrations api
python manage.py migrate
```

## 📌 Paso 7: Crear un serializador

Creamos `api/serializers.py`:

```python
from rest_framework import serializers
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
```

## 📌 Paso 8: Crear vistas para la API

Editamos `api/views.py`:

```python
from rest_framework import viewsets
from .models import Item
from .serializers import ItemSerializer

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
```

## 📌 Paso 9: Configurar las URLs de la API

Editamos `api/urls.py`:

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet

router = DefaultRouter()
router.register(r'items', ItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```

Y `apiserver/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
```

## 📌 Paso 10: Probar el servidor

```bash
python manage.py runserver 0.0.0.0:8000
```

- Ver items: [http://localhost:8000/api/items/](http://localhost:8000/api/items/)
- Panel de administración: [http://localhost:8000/admin/](http://localhost:8000/admin/)

Crear un usuario administrador:

```bash
python manage.py createsuperuser
```

## 📌 Paso 11: Desplegar en producción

1️⃣ Instalar Gunicorn:

```bash
pip install gunicorn
gunicorn --bind 0.0.0.0:8000 apiserver.wsgi
```

2️⃣ Instalar y configurar Nginx:

```bash
sudo apt install nginx -y
```

Archivo de configuración en `/etc/nginx/sites-available/django_api`:

```nginx
server {
    listen 80;
    server_name tu-servidor;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

Habilitar sitio y reiniciar Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/django_api /etc/nginx/sites-enabled
sudo systemctl restart nginx
```

## 📌 Conclusión

Tu API REST con Django está lista y funcionando en un servidor Debian con Gunicorn y NGINX. 🚀
