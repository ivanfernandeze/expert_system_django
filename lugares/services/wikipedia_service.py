import requests
import os
from django.conf import settings
from urllib.parse import urlparse
from django.core.files import File
from io import BytesIO

class WikipediaService:
    HEADERS = {
        'User-Agent': 'AdivinaTurExpert/1.0 (local usage)'
    }

    @staticmethod
    def obtener_descripcion_imagen(nombre_lugar):
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
            R = S.get(url=URL, params=PARAMS, headers=WikipediaService.HEADERS)
            R.raise_for_status()
            DATA = R.json()

            pages = DATA['query']['pages']
            for page_id, page in pages.items():
                if 'missing' in page:
                    return None, None
                descripcion = page.get('extract', '')
                imagen_url = page.get('original', {}).get('source', None)
                return descripcion, imagen_url

        except requests.exceptions.RequestException:
            return None, None

    @staticmethod
    def descargar_imagen(imagen_url, nombre_lugar):
        try:
            response = requests.get(imagen_url, stream=True)
            response.raise_for_status()
            image_content = BytesIO(response.content)
            # extraer extension 
            parsed_url = urlparse(imagen_url)
            extension = os.path.splitext(parsed_url.path)[1]
            nombre_imagen = f"{nombre_lugar}{extension}"
            return nombre_imagen, image_content
        except requests.exceptions.RequestException:
            return None, None
