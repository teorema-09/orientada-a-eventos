from rest_framework import viewsets
from .models import Motocicleta
from .serializers import MotocicletaSerializer


class MotocicletaViewSet(viewsets.ModelViewSet):
    queryset = Motocicleta.objects.all()
    serializer_class = MotocicletaSerializer
    # Look up objects by 'placa' (unique field) instead of the numeric PK
    lookup_field = 'placa'
    # Optional: restrict allowed characters for the lookup in the URL (alphanumeric, no spaces)
    lookup_value_regex = r'[A-Za-z0-9]+'

