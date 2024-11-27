import requests
from lxml import html
from django.core.management.base import BaseCommand
from models import Url_Locales, SelectorMAPA, Mapa_data

class Command(BaseCommand):
    help = "Realiza scraping de las URLs almacenadas en la base de datos."

    def handle(self, *args, **kwargs):
        # Obtiene todas las URLs con sus selectores
        urls = Url_Locales.objects.prefetch_related('selectors').all()
        for url_obj in urls:
            url = url_obj.url
            selectors = url_obj.selectors.all()

            if not selectors.exists():
                self.stdout.write(self.style.WARNING(f"No hay selectores para la URL: {url}"))
                continue

            try:
                # Realiza la solicitud
                response = requests.get(url)
                response.raise_for_status()
                tree = html.fromstring(response.content)
                
                for selector in selectors:
                    # Realiza el scraping
                    local = tree.cssselect(selector.local_selector)
                    direccion = tree.cssselect(selector.direccion_selector)

                    # Procesa los datos si existen
                    local_text = local[0].text_content().strip() if local else "No encontrado"
                    direccion_text = direccion[0].text_content().strip() if direccion else "No encontrado"

                    # Guarda en la base de datos
                    Mapa_data.objects.create(
                        local=local_text,
                        direccion=direccion_text,
                        url=url_obj
                    )

                    self.stdout.write(self.style.SUCCESS(f"Datos guardados: {local_text} - {direccion_text}"))

            except requests.RequestException as e:
                self.stdout.write(self.style.ERROR(f"Error al solicitar {url}: {e}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error general al procesar {url}: {e}"))
