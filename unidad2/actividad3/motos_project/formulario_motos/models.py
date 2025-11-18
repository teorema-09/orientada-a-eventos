from django.db import models
class Motocicleta(models.Model):  
    placa = models.CharField(max_length=10, unique=True) 
    propietario = models.CharField(max_length=100) 
    cilindraje = models.PositiveIntegerField()
    fecha_fabricacion = models.DateField()

    def _str_(self):
        return f"{self.placa} - {self.propietario}"


