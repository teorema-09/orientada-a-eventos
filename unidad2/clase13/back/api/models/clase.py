from django.db import models

class Clase(models.Model):
	
	tema = models.CharField(max_length = 50, null = False, blank = True)
	descripcion = models.TextField(max_length = 5000, null = False, blank = True)
	fecha = models.DateTimeField(auto_now = True, verbose_name = "date updated")
	numero_clase = models.IntegerField()
	
	def __str__(self):
		return self.tema