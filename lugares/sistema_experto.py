from experta import Fact, KnowledgeEngine, Rule, MATCH, Field
from lugares.models import Destino

class PreferenciaUsuario(Fact):
    clima = Field(str, default="" )
    actividad = Field(str, default="")
    presupuesto = Field(str, default="")
    duracion = Field(str, default="")
    preferencias_culturales = Field(str, default="")
    edad_recomendada = Field(str, default="")
    idioma_local = Field(str, default="")

class RecomendacionEngine(KnowledgeEngine):
    def __init__(self, preferencias):
        super(RecomendacionEngine, self).__init__()
        self.preferencias = preferencias
        self.recomendaciones = []

    @Rule(PreferenciaUsuario(
        clima=MATCH.clima,
        actividad=MATCH.actividad,
        presupuesto=MATCH.presupuesto,
        duracion=MATCH.duracion,    
        preferencias_culturales=MATCH.pref_cult,
        edad_recomendada=MATCH.edad,
        idioma_local=MATCH.idioma
    ))
    
    def evaluar_preferencias(self, clima, actividad, presupuesto, duracion, pref_cult, edad, idioma):
        pesos = {
            "clima": 2,
            "actividades": 4,
            "presupuesto": 3,
            "duracion": 1,
            "preferencias_culturales": 3,
            "edad_recomendada": 2,
            "idioma_local": 1
        }
        destinos = Destino.objects.all()
        mejor_puntaje = 0
        puntuaciones = []

        for destino in destinos:
            puntaje = 0
            if clima in destino.clima:
                puntaje += pesos.get('clima', 0)
            if actividad in destino.actividades:
                puntaje += pesos.get('actividades', 0)
            if presupuesto in destino.presupuesto:
                puntaje += pesos.get('presupuesto', 0)
            if duracion in destino.presupuesto:
                puntaje += pesos.get('duracion', 0)
            if pref_cult in destino.preferencias_culturales:
                puntaje += pesos.get('preferencias_culturales', 0)
            if edad in destino.edad_recomendada:
                puntaje += pesos.get('edad_recomendada', 0)
            if idioma in destino.idioma_local:
                puntaje += pesos.get('idioma_local', 0)

            puntuaciones.append((destino, puntaje))
            if puntaje > mejor_puntaje:
                mejor_puntaje = puntaje

        # Selecciona destinos con puntaje dentro del 80% del mejor puntaje
        umbral = 0.8 * mejor_puntaje
        self.recomendaciones = [
            {"destino": destino, "puntaje": puntaje} 
            for destino, puntaje in puntuaciones 
            if puntaje >= umbral
        ]

    def obtener_recomendaciones(self):
        return self.recomendaciones
