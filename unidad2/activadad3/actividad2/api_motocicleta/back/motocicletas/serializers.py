from rest_framework import serializers
from .models import Motocicleta


class MotocicletaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motocicleta
        fields = ['id', 'placa', 'propietario', 'cilindrage', 'fecha_fabricacion']
