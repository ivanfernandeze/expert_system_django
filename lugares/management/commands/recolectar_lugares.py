
from django.core.management.base import BaseCommand
import requests
import os
from urllib.request import urlretrieve

from lugares.models import LugarTuristico
from lugares.scripts.lugares_lista import LUGARES

class Command(BaseCommand):
    help = 'Recolectar lugares'

    def handle(self, *args, **kwargs):
        HEADERS = {
            'User-Agent': 'AdivinaTurExpert/1.0 (local usage)'
        }

        def obtener_descripcion(nombre_lugar):
            """
            descripcion de wikipedia
            """
            S = requests.Session()

            URL = "https://es.wikipedia.org/w/api.php"

            PARAMS = {
                "action": "query",
                "format": "json",
                "titles": nombre_lugar,
                "prop": "extracts|pageimages",
                "exintro": True,
                "explaintext": True,
                "piprop": "original",
                "redirects": 1
            }

            try:
                R = S.get(url=URL, params=PARAMS, headers=HEADERS)
                R.raise_for_status()
                DATA = R.json()

                pages = DATA['query']['pages']
                for page_id, page in pages.items():
                    if 'missing' in page:
                        self.stdout.write(self.style.WARNING(f"Artículo '{nombre_lugar}' no encontrado."))
                        return None, None
                    descripcion = page.get('extract', '')
                    imagen_url = page.get('original', {}).get('source', None)
                    return descripcion, imagen_url

            except requests.exceptions.RequestException as e:
                self.stdout.write(self.style.ERROR(f"Error al obtener datos para '{nombre_lugar}': {e}"))
                return None, None

        def guardar_lugar(nombre, descripcion, imagen_url):
            """
            Guardar lugar turistico
            """
            lugar, created = LugarTuristico.objects.get_or_create(nombre=nombre)
            lugar.descripcion = descripcion

            if imagen_url:
                try:
                    imagen_nombre = os.path.basename(imagen_url)
                    imagen_path = os.path.join('imagenes_lugares', imagen_nombre)

                    media_root = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '../../media')
                    imagen_full_path = os.path.join(media_root, 'imagenes_lugares')

                    os.makedirs(imagen_full_path, exist_ok=True)

                    archivo_destino = os.path.join(imagen_full_path, imagen_nombre)

                    if not os.path.exists(archivo_destino):
                        urlretrieve(imagen_url, archivo_destino)
                        self.stdout.write(self.style.SUCCESS(f"Imagen descargada: {archivo_destino}"))
                    else:
                        self.stdout.write(self.style.WARNING(f"La imagen ya existe: {archivo_destino}"))

                    lugar.imagen = os.path.join('imagenes_lugares', imagen_nombre)

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error al descargar la imagen para '{nombre}': {e}"))

            lugar.save()
            if created:
                self.stdout.write(self.style.SUCCESS(f"Lugar turístico '{nombre}' agregado a la base de datos."))
            else:
                self.stdout.write(self.style.SUCCESS(f"Lugar turístico '{nombre}' actualizado en la base de datos."))

        def recolectar_datos():
            """
            Recolecta datos de LUGARES[]
            """
            for nombre_lugar in LUGARES:
                self.stdout.write(f"Procesando '{nombre_lugar}'...")
                descripcion, imagen_url = obtener_descripcion(nombre_lugar)
                if descripcion:
                    guardar_lugar(nombre_lugar, descripcion, imagen_url)
                else:
                    self.stdout.write(self.style.WARNING(f"No se pudo obtener descripción para '{nombre_lugar}'."))

        recolectar_datos()
