# myapp/management/commands/scrape_views.py
from django.core.management.base import BaseCommand
from models import PageSelector
from bs4 import BeautifulSoup
import requests

class Command(BaseCommand):
    help = 'Scrapea datos según selectores especificados'

    def handle(self, *args, **kwargs):
        # Obtén todos los selectores
        selectores = PageSelector.objects.all()
        results = {}

        for selector in selectores:
            url = selector.url.url
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Scrapea los datos según los selectores
            data = {
                'product': [element.get_text() for element in soup.select(selector.product_selector)],
                'price': [element.get_text() for element in soup.select(selector.price_selector)],
                'description': [element.get_text() for element in soup.select(selector.description_selector)],
                'image': [element['src'] for element in soup.select(selector.image_selector)],
                'logo': [element['src'] for element in soup.select(selector.logo_selector)],
            }
            results[url] = data

        return results  # O guarda en la base de datos según necesites
