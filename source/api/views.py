from rest_framework import viewsets

from juego import models as juego_m
from api import serializers as juego_s


class SemanaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para las :class:`Semana`.
    """
    queryset = juego_m.Semana.objects.all()
    serializer_class = juego_s.SemanaSerializer
