from lugares.sistema_experto import RecomendacionEngine, PreferenciaUsuario

def obtener_recomendaciones(preferencias):
    engine = RecomendacionEngine(preferencias)
    engine.declare(PreferenciaUsuario(
        clima=preferencias.get('clima', ''),
        actividad=preferencias.get('actividad', ''),
        presupuesto=preferencias.get('presupuesto', ''),
        duracion=preferencias.get('duracion', ''),
        preferencias_culturales=preferencias.get('preferencias_culturales', ''),
        edad_recomendada=preferencias.get('edad_recomendada', ''),
        idioma_local=preferencias.get('idioma_local', '')
    ))
    engine.run()
    destinos = engine.obtener_recomendaciones()

    recomendaciones = []
    max_puntaje = max(destino["puntaje"] for destino in destinos) if destinos else 1  # evitar división por cero

    for destino_info in destinos:
        destino = destino_info["destino"]
        puntaje = destino_info["puntaje"]
        descripcion = destino.descripcion if destino.descripcion else "Descripción no disponible."
        imagen_url = destino.imagen if destino.imagen else "https://via.placeholder.com/300x200.png?text=Sin+Imagen"
        
        # porcentaje de precision
        porcentaje_precision = (puntaje / max_puntaje) * 100
        recomendaciones.append({
            'nombre': destino.nombre,
            'descripcion': descripcion,
            'imagen_url': imagen_url,
            'porcentaje_precision': round(porcentaje_precision, 2)
        })

    return recomendaciones
