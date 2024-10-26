# lugares/views.py

from django.shortcuts import render
from .forms import PreferenciasForm
from .services.sistema_experto_service import obtener_recomendaciones


def recomendar_lugar(request):
    recomendaciones = []
    mensaje = ""
    if request.method == 'POST':
        form = PreferenciasForm(request.POST)
        if form.is_valid():
            categoria = form.cleaned_data['categoria']
            clima = form.cleaned_data['clima']
            presupuesto = form.cleaned_data['presupuesto']
            recomendaciones = obtener_recomendaciones(categoria, clima, presupuesto)
            if not recomendaciones:
                mensaje = "Lo siento, no tenemos recomendaciones para tus preferencias."
    else:
        form = PreferenciasForm()

    context = {
        'form': form,
        'recomendaciones': recomendaciones,
        'mensaje': mensaje
    }
    return render(request, 'lugares/recomendar_lugar.html', context)
