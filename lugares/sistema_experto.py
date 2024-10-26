from experta import Fact, KnowledgeEngine, Rule, MATCH, Field
from lugares.models import LugarTuristico

class PreferenciaUsuario(Fact):
    categoria = Field(str, default="")
    clima = Field(str, default="")
    presupuesto = Field(str, default="")

class RecomendacionEngine(KnowledgeEngine):
    def __init__(self):
        super(RecomendacionEngine, self).__init__()
        self.recomendaciones = []

    @Rule(PreferenciaUsuario(categoria='aventura', clima='templado', presupuesto='medio'))
    def recomendar_machu_picchu(self):
        self.recomendaciones.append("Machu Picchu")

    @Rule(PreferenciaUsuario(categoria='cultural', clima='templado', presupuesto='alto'))
    def recomendar_torre_eiffel(self):
        self.recomendaciones.append("Torre Eiffel")

    @Rule(PreferenciaUsuario(categoria='relajación', clima='caliente', presupuesto='medio'))
    def recomendar_santorini(self):
        self.recomendaciones.append("Santorini")


    def obtener_recomendaciones_usuario(self, categoria, clima, presupuesto):
        self.reset()
        self.declare(PreferenciaUsuario(categoria=categoria, clima=clima, presupuesto=presupuesto))
        self.run()
        return self.recomendaciones
