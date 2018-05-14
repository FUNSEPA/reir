from rest_framework import serializers

from juego import models as juego_m


class DepartamentoSerializer(serializers.ModelSerializer):
    puntos = serializers.FloatField()

    class Meta:
        model = juego_m.Departamento
        fields = '__all__'


class SemanaSerializer(serializers.ModelSerializer):
    puntos_equipo = serializers.SerializerMethodField()

    class Meta:
        model = juego_m.Semana
        fields = '__all__'

    def get_puntos_equipo(self, obj):
        return DepartamentoSerializer(obj.puntos_equipo().values(), many=True).data
