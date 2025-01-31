from django.shortcuts import render
from rest_framework import viewsets
from .models import Item, Persona
from .serializers import ItemSerializer,PersonaSerializer

# Create your views here.
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

# Create your views here.
class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer
