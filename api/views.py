from django.shortcuts import render
from rest_framework import viewsets
from .models import Item, Persona
from .serializers import ItemSerializer,PersonaSerializer

import os
from openai import OpenAI

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from dotenv import load_dotenv

# Cargar las variables de entorno del archivo .env
load_dotenv()


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
DEBUG = os.getenv("DEBUG") == "True"

# Create your views here.
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

# Create your views here.
class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer

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