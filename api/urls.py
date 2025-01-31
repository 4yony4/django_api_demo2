from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet,PersonaViewSet

router = DefaultRouter()
router.register(r'items', ItemViewSet)
router.register(r'personas', PersonaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]