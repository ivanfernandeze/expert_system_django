from lugares.sistema_experto import RecomendacionEngine
from lugares.models import LugarTuristico


def obtener_recomendaciones(categoria, clima, presupuesto):
    engine = RecomendacionEngine()
    destinos = engine.obtener_recomendaciones_usuario(categoria, clima, presupuesto)

    lugares = []
    for destino in destinos:
        try:
            lugar = LugarTuristico.objects.get(nombre=destino)
            lugares.append(lugar)
        except LugarTuristico.DoesNotExist:
            pass

    return lugares
