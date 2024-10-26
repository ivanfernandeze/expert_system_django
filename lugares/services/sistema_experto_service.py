from lugares.sistema_experto import RecomendacionEngine, PreferenciaUsuario

def obtener_recomendaciones(preferencias):
    """
    :param preferencias: dict con las preferencias del usuario.
    :return: lista de dicts con destino, descripcion, imagen_url.
    """
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
    for destino in destinos:
        descripcion = destino.descripcion if destino.descripcion else "Descripción no disponible."
        if destino.imagen:
            imagen_url = destino.imagen
        else:
            imagen_url = "https://via.placeholder.com/300x200.png?text=Sin+Imagen"
        recomendaciones.append({
            'nombre': destino.nombre,
            'descripcion': descripcion,
            'imagen_url': imagen_url
        })

    return recomendaciones
