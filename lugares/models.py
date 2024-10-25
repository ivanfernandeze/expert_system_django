from django.db import models


class LugarTuristico(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='imagenes_lugares/', blank=True, null=True)

    def __str__(self):
        return self.nombre
