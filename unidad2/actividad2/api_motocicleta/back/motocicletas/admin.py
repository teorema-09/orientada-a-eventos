from django.contrib import admin
from .models import Motocicleta


@admin.register(Motocicleta)
class MotocicletaAdmin(admin.ModelAdmin):
	list_display = ('placa', 'propietario', 'cilindrage', 'fecha_fabricacion')
	search_fields = ('placa', 'propietario')
