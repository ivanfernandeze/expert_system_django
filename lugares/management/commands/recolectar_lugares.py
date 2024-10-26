import json
from django.core.management.base import BaseCommand
from lugares.models import Destino
import os
from lugares.services.wikipedia_service import WikipediaService
from django.core.files import File

class Command(BaseCommand):
    help = 'Carga destinos turísticos desde un archivo JSON y obtiene descripción e imagen desde Wikipedia'

    def add_arguments(self, parser):
        parser.add_argument(
            '--archivo',
            type=str,
            help='Ruta al archivo destinos.json',
            default='lugares/scripts/destinos.json'
        )

    def handle(self, *args, **kwargs):
        archivo = kwargs['archivo']
        if not os.path.exists(archivo):
            self.stderr.write(self.style.ERROR(f'Archivo {archivo} no encontrado.'))
            return

        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError:
            self.stderr.write(self.style.ERROR(f'Error al decodificar JSON en {archivo}.'))
            return

        for nombre, atributos in data.items():
            self.stdout.write(f"Procesando '{nombre}'...")
            clima = atributos.get('clima', [])
            actividades = atributos.get('actividades', [])
            presupuesto = atributos.get('presupuesto', [])
            preferencias_culturales = atributos.get('preferencias_culturales', [])
            edad_recomendada = atributos.get('edad_recomendada', [])
            idioma_local = atributos.get('idioma_local', [])

            descripcion, imagen_url = WikipediaService.obtener_descripcion_imagen(nombre)

            defaults = {
                'clima': clima,
                'actividades': actividades,
                'presupuesto': presupuesto,
                'preferencias_culturales': preferencias_culturales,
                'edad_recomendada': edad_recomendada,
                'idioma_local': idioma_local,
                'descripcion': descripcion if descripcion else "Descripción no disponible.",
            }

            try:
                destino, created = Destino.objects.update_or_create(
                    nombre=nombre,
                    defaults=defaults
                )

                if imagen_url:
                    nombre_imagen, image_content = WikipediaService.descargar_imagen(imagen_url, nombre)
                    if nombre_imagen and image_content:
                        destino.imagen.save(nombre_imagen, File(image_content), save=True)
                        self.stdout.write(self.style.SUCCESS(f"Imagen para '{nombre}' guardada correctamente."))
                    else:
                        self.stdout.write(self.style.WARNING(f"No se pudo descargar la imagen para '{nombre}'."))
                else:
                    self.stdout.write(self.style.WARNING(f"No se encontró una imagen para '{nombre}'."))

                if created:
                    self.stdout.write(self.style.SUCCESS(f'Destino "{nombre}" creado correctamente.'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Destino "{nombre}" actualizado correctamente.'))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error al crear/actualizar '{nombre}': {e}"))
