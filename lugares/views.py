from django.shortcuts import render, redirect
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


def prueba(request):
    return render(request, 'base.html')

def preguntas_view(request):
    # Diccionario con las preguntas y opciones
    preguntas = {
        "clima": {
            "cálido": ["húmedo", "seco"],
            "frío": ["polar", "templado"],
            "desértico": ["árido", "semiárido"],
            "tropical": ["húmedo", "seco"],
            "marítimo": ["mediterráneo", "oceánico"]
        },
        "actividades": {
            "deportes": ["rafting", "windsurf", "escalada", "esquí", "deportes acuáticos", "deportes extremos"],
            "cultura": ["observación de cóndores", "visitas culturales", "cultura indígena", "turismo histórico", "observación de estrellas", "observación de glaciares"],
            "naturaleza": ["observación de flora", "observación de fauna", "camping", "observación de la naturaleza"],
            "aventura": ["senderismo", "caminatas", "paseos en cerro", "exploración de ruinas", "paseos en buggy", "sandboarding"],
            "relajación": ["playa", "vida nocturna", "pesca", "fotografía", "compras de artesanías", "compras", "gastronomía"]
        },
        "presupuesto": ["bajo", "medio", "alto"],
        "preferencias_culturales": {
            "arte y cultura": ["arte", "artesanía", "arquitectura"],
            "ciencia y religión": ["ciencia", "religión"],
            "naturaleza y aventura": ["naturaleza", "aventura"],
            "historia y gastronomía": ["historia", "gastronomía"]
        },
        "edad_recomendada": ["niños", "jóvenes", "adultos"],
        "idioma_local": ["español", "inglés", "quechua", "portugués", "rapa nui"]
    }
    if request.method == "POST":
        # Guardar preferencias en la sesión
        for key in preguntas.keys():
            if key in request.POST:
                request.session[key] = request.POST[key]

        # Debug: Imprimir datos de la sesión
        print("Datos de la sesión:", request.session.items())


        # Si ya se han respondido todas las preguntas, obtener recomendaciones
        if len(request.session.keys()) == len(preguntas):
            recomendaciones = obtener_recomendaciones(request.session)
            print("Recomendaciones:", recomendaciones)
            # limitar a 3 recomendaciones si es que tiene mas de 3
            if len(recomendaciones) > 4:
                recomendaciones = recomendaciones[:4]
            request.session.clear()
            return render(request, 'resultados.html', {'recomendaciones': recomendaciones})

        # Si aún no han respondido todas las preguntas, avanzar
        return redirect('preguntas')

    # Obtener la siguiente pregunta
    preguntas_restantes = {k: v for k, v in preguntas.items() if k not in request.session}

    if preguntas_restantes:
        pregunta_actual = next(iter(preguntas_restantes))
        opciones = preguntas_restantes[pregunta_actual]
    else:
        pregunta_actual = None
        opciones = []

    return render(request, 'preguntar.html', {'pregunta': pregunta_actual, 'opciones': opciones})


def resultados_view(request):
    return render(request, 'resultados.html', {'recomendaciones': [
        {'nombre': 'Serra do Rio do Rastro', 'descripcion': "Serra do Rio do Rastro (IPA: [ˈsɛʁɘ du 'ʁiu du 'ʁastɾu], literalmente Sierra del Río del Rastro) es una sierra ubicada en el sudeste del estado de Santa Catarina, en la Región Sur de Brasil. La carretera SC-390 pasa por esta sierra, que tiene paisajes memorables y grandes peñones.\nEsta sierra está situada entre los municipios de Lauro Müller y Bom Jardim da Serra y su punto más alto está situado a 1.460 metros sobre el nivel del mar. En las partes más elevadas de esta sierra, el océano Atlántico, ubicado a cerca de 100 km de distancia, puede ser visto. Son comunes las heladas  y puede nevar en sus partes más altas.", 'imagen_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/71/Mares_de_Morros_Catarinenses.jpg/320px-Mares_de_Morros_Catarinenses.jpg', 'porcentaje_precision': 100.0}
        ,{'nombre': 'Serra do Rio do Rastro', 'descripcion': "Serra do Rio do Rastro (IPA: [ˈsɛʁɘ du 'ʁiu du 'ʁastɾu], literalmente Sierra del Río del Rastro) es una sierra ubicada en el sudeste del estado de Santa Catarina, en la Región Sur de Brasil. La carretera SC-390 pasa por esta sierra, que tiene paisajes memorables y grandes peñones.\nEsta sierra está situada entre los municipios de Lauro Müller y Bom Jardim da Serra y su punto más alto está situado a 1.460 metros sobre el nivel del mar. En las partes más elevadas de esta sierra, el océano Atlántico, ubicado a cerca de 100 km de distancia, puede ser visto. Son comunes las heladas  y puede nevar en sus partes más altas.", 'imagen_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/71/Mares_de_Morros_Catarinenses.jpg/320px-Mares_de_Morros_Catarinenses.jpg', 'porcentaje_precision': 100.0}
        ,{'nombre': 'Serra do Rio do Rastro', 'descripcion': "Serra do Rio do Rastro (IPA: [ˈsɛʁɘ du 'ʁiu du 'ʁastɾu], literalmente Sierra del Río del Rastro) es una sierra ubicada en el sudeste del estado de Santa Catarina, en la Región Sur de Brasil. La carretera SC-390 pasa por esta sierra, que tiene paisajes memorables y grandes peñones.\nEsta sierra está situada entre los municipios de Lauro Müller y Bom Jardim da Serra y su punto más alto está situado a 1.460 metros sobre el nivel del mar. En las partes más elevadas de esta sierra, el océano Atlántico, ubicado a cerca de 100 km de distancia, puede ser visto. Son comunes las heladas  y puede nevar en sus partes más altas.", 'imagen_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/71/Mares_de_Morros_Catarinenses.jpg/320px-Mares_de_Morros_Catarinenses.jpg', 'porcentaje_precision': 100.0}
        ,{'nombre': 'Serra do Rio do Rastro', 'descripcion': "Serra do Rio do Rastro (IPA: [ˈsɛʁɘ du 'ʁiu du 'ʁastɾu], literalmente Sierra del Río del Rastro) es una sierra ubicada en el sudeste del estado de Santa Catarina, en la Región Sur de Brasil. La carretera SC-390 pasa por esta sierra, que tiene paisajes memorables y grandes peñones.\nEsta sierra está situada entre los municipios de Lauro Müller y Bom Jardim da Serra y su punto más alto está situado a 1.460 metros sobre el nivel del mar. En las partes más elevadas de esta sierra, el océano Atlántico, ubicado a cerca de 100 km de distancia, puede ser visto. Son comunes las heladas  y puede nevar en sus partes más altas.", 'imagen_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/71/Mares_de_Morros_Catarinenses.jpg/320px-Mares_de_Morros_Catarinenses.jpg', 'porcentaje_precision': 100.0}
    ]})