from django.db import models


class Motocicleta(models.Model):
    placa = models.CharField(max_length=20, unique=True)
    propietario = models.CharField(max_length=100)
    cilindrage = models.PositiveIntegerField()
    fecha_fabricacion = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.placa} - {self.propietario}"

