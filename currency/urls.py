from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import CurrencyViewSet

router = DefaultRouter()
router.register(r'currency', CurrencyViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
