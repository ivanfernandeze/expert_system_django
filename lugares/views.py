from django.shortcuts import render
from .forms import PreferenciasForm
from .services.sistema_experto_service import obtener_recomendaciones

def recomendar_lugar(request):
    recomendaciones = []
    mensaje = ""
    if request.method == 'POST':
        form = PreferenciasForm(request.POST)
        if form.is_valid():
            preferencias = {
                'clima': form.cleaned_data['clima'],
                'actividad': form.cleaned_data['actividad'],
                'presupuesto': form.cleaned_data['presupuesto'],
                'duracion': form.cleaned_data['duracion'],
                'preferencias_culturales': form.cleaned_data['preferencias_culturales'],
                'edad_recomendada': form.cleaned_data['edad_recomendada'],
                'idioma_local': form.cleaned_data['idioma_local'],
            }
            recomendaciones = obtener_recomendaciones(preferencias)
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
