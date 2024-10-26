# lugares/services/wikipedia_service.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os

class WikipediaService:
    HEADERS = {
        'User-Agent': 'AdivinaTurExpert/1.0 (local usage)'
    }

    @staticmethod
    def obtener_descripcion(nombre_lugar):
        """
        Obtiene la descripción de Wikipedia para un lugar turístico utilizando la API de Wikipedia.
        """
        S = requests.Session()
        API_URL = "https://es.wikipedia.org/w/api.php"

        PARAMS = {
            "action": "query",
            "format": "json",
            "titles": nombre_lugar,
            "prop": "extracts",
            "exintro": True,
            "explaintext": True,
            "redirects": 1
        }

        try:
            R = S.get(url=API_URL, params=PARAMS, headers=WikipediaService.HEADERS)
            R.raise_for_status()
            DATA = R.json()

            pages = DATA['query']['pages']
            for page_id, page in pages.items():
                if 'missing' in page:
                    # La página no existe
                    return None
                descripcion = page.get('extract', '')
                return descripcion

        except requests.exceptions.RequestException as e:
            print(f"Error al obtener descripción de Wikipedia para '{nombre_lugar}': {e}")
            return None

    @staticmethod
    def obtener_primera_imagen(nombre_lugar):
        """
        Obtiene la primera imagen encontrada en la página de Wikipedia del lugar turístico.
        """
        S = requests.Session()
        page_title = nombre_lugar.replace(' ', '_')
        page_url = f"https://es.wikipedia.org/wiki/{page_title}"

        try:
            R_html = S.get(url=page_url, headers=WikipediaService.HEADERS)
            R_html.raise_for_status()
            soup = BeautifulSoup(R_html.content, 'html.parser')

            # Buscar todas las etiquetas img dentro del contenido de la página
            content_div = soup.find('div', id='mw-content-text')
            if not content_div:
                return None

            img_tag = content_div.find('img')
            if not img_tag:
                return None

            img_src = img_tag.get('src')
            if not img_src:
                return None

            # Manejar URLs que comienzan con '//'
            if img_src.startswith('//'):
                img_url = f"https:{img_src}"
            elif img_src.startswith('/'):
                img_url = f"https://es.wikipedia.org{img_src}"
            else:
                img_url = img_src

            return img_url

        except requests.exceptions.RequestException as e:
            print(f"Error al obtener imagen de Wikipedia para '{nombre_lugar}': {e}")
            return None

    @staticmethod
    def obtener_descripcion_imagen(nombre_lugar):
        """
        Combina obtener_descripcion y obtener_primera_imagen.
        Retorna descripción y URL de la primera imagen encontrada.
        """
        descripcion = WikipediaService.obtener_descripcion(nombre_lugar)
        imagen_url = WikipediaService.obtener_primera_imagen(nombre_lugar)
        return descripcion, imagen_url
