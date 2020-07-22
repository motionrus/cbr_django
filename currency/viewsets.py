from rest_framework import viewsets
from .models import Currency
from .serializers import CurrencySerializer


class CurrencyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Currency.objects.prefetch_related("currencies")
    serializer_class = CurrencySerializer
