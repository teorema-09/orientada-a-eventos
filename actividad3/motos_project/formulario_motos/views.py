from django.shortcuts import render, redirect , get_object_or_404
from .models import Motocicleta

def crear_motocicleta(request):
    if request.method == 'POST':
        placa = request.POST.get('placa')
        propietario = request.POST.get('propietario')
        cilindraje = request.POST.get('cilindraje')
        fecha_fabricacion = request.POST.get('fecha_fabricacion')
        motocicleta = Motocicleta(
            placa=placa,
            propietario=propietario,
            cilindraje=cilindraje,
            fecha_fabricacion=fecha_fabricacion
        )
        motocicleta.save()
        return redirect('lista_motocicletas')
    return render(request, 'formulario_motos/crear_motocicleta.html')




def lista_motocicletas(request):
    motos = Motocicleta.objects.all()
    return render(request, 'formulario_motos/lista_motocicletas.html', {'motos': motos})



def eliminar_motocicleta(request, moto_id):
    moto = get_object_or_404(Motocicleta, id=moto_id)
    moto.delete()
    return redirect('lista_motocicletas')