
# 🌐 Integración de la API de OpenAI en Django

Este proyecto muestra cómo integrar la **API de OpenAI** en un servidor **Django** utilizando un endpoint de API REST para enviar consultas y recibir respuestas.

---

## 🚀 1️⃣ Instalación de Dependencias

Instala la librería oficial de OpenAI en tu entorno virtual:

```bash
pip install openai
```

---

## 🔐 2️⃣ Configuración de la Clave API de OpenAI

Obtén tu clave API en [https://platform.openai.com/](https://platform.openai.com/).

Guárdala como una variable de entorno:

```bash
export OPENAI_API_KEY="tu_clave_api_aqui"
```

O usa un archivo `.env` para cargarla automáticamente (requiere `python-dotenv`):

```bash
pip install python-dotenv
```

Archivo `.env`:

```
OPENAI_API_KEY=tu_clave_api_aqui
```

---

## 📡 3️⃣ Creación del Endpoint en Django

### a) Modificar `views.py`

```python
from django.shortcuts import render
from rest_framework import viewsets
from .models import Item, Persona
from .serializers import ItemSerializer,PersonaSerializer

import os
from openai import OpenAI

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# Cargar la API Key desde una variable de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")

class OpenAIChatView(APIView):
    def post(self, request):
        prompt = request.data.get('prompt')  # Recibimos el prompt del usuario

        if not prompt:
            return Response(
                {"error": "El campo 'prompt' es requerido."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Llamada a la API de OpenAI usando el nuevo endpoint para Chat Completions
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "developer", "content": "You are a helpful assistant."},
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # Devolver la respuesta de OpenAI
            return Response({
                "prompt": prompt,
                "respuesta": response.choices[0].message.content
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
```

---

### b) Configurar las URLs

Edita `api/urls.py`:

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet, OpenAIChatView

router = DefaultRouter()
router.register(r'items', ItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('openai/chat/', OpenAIChatView.as_view(), name='openai_chat'),
]
```

---

## 🔍 4️⃣ Probar el Endpoint

Ejecuta el servidor:

```bash
python manage.py runserver
```

### ✅ Realizar una consulta:

```bash
curl -X POST http://localhost:8000/api/openai/chat/ \
     -H "Content-Type: application/json" \
     -d '{"prompt": "¿Cuál es la capital de Francia?"}'
```

### ✅ Respuesta esperada:

```json
{
    "prompt": "¿Cuál es la capital de Francia?",
    "respuesta": "La capital de Francia es París."
}
```

---

## 🚀 5️⃣ Mejoras opcionales

Para gestionar mejor la API Key, usa `python-dotenv`:

```bash
pip install python-dotenv
```

Carga las variables en `views.py`:

```python
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
```

---

## 🎯 Conclusión

Ahora tu API REST de Django puede interactuar con OpenAI para enviar consultas y obtener respuestas en tiempo real. 🌍✨
