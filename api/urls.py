from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet,PersonaViewSet,OpenAIChatView

router = DefaultRouter()
router.register(r'items', ItemViewSet)
router.register(r'personas', PersonaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('openai/chat/', OpenAIChatView.as_view(), name='openai_chat'),  # Nueva ruta
]