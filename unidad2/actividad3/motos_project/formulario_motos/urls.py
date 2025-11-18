from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_motocicletas, name='lista_motocicletas'),
    path('crear/', views.crear_motocicleta, name='crear_motocicleta'),
    path('eliminar/<int:moto_id>/', views.eliminar_motocicleta, name='eliminar_motocicleta'),
]
