from django.db import models

class Destino(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    clima = models.JSONField()
    actividades = models.JSONField()
    presupuesto = models.JSONField()
    preferencias_culturales = models.JSONField()
    edad_recomendada = models.JSONField()
    idioma_local = models.JSONField()
    descripcion = models.TextField(blank=True, null=True)
    imagen = models.ImageField(upload_to='imagenes_lugares/', blank=True, null=True)  

    def __str__(self):
        return self.nombre
