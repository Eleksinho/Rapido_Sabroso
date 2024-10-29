from django.core.management.base import BaseCommand
from lxml import html
import requests

# Definición de categorías y selectores predeterminados
CATEGORIAS = {
    'Hamburguesa': ['hamburguesa', 'burger'],
    'Pizza': ['pizza'],
    'Bebidas': ['bebida', 'drink', 'drinks'],
    'Burritos': ['burrito'],
    'Pollo': ['pollo', 'chicken'],
    'Empanadas': ['empanada'],
    'Sandwiches': ['sandwich'],
    'Combos': ['combo'],
    'Papas Fritas': ['papas fritas', 'papas', 'fritas'],
    'Sin Categoría': []
}

DEFAULT_SELECTORS = {
    'producto': "//span[@class='line-clamp-2']",
    'precio': "//div[@class='flex gap-x-2 text-sm flex-row']/div[1]/text()",
    'descripcion': "//p[contains(@class, 'mt-0.5') and contains(@class, 'line-clamp-3')]",
    'imagen': "//img[contains(@src, 'tofuu') and @class='rounded-l-lg']/@src",
    'logo': "//span//img[contains(@src, 'tofuu')]/@src"
}

class Command(BaseCommand):
    help = 'Realiza scraping de una URL específica sin guardar los datos'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str, help='URL para realizar el scraping')

    def handle(self, *args, **options):
        url = options['url']
        self.stdout.write(f"Scraping {url}...")

        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            self.stdout.write(self.style.ERROR(f"Error al acceder a {url}: {e}"))
            return

        tree = html.fromstring(response.content)

        # Obtener productos, precios, descripciones e imágenes usando selectores
        productos = tree.xpath(DEFAULT_SELECTORS['producto'])
        precios = tree.xpath(DEFAULT_SELECTORS['precio'])
        descripciones = tree.xpath(DEFAULT_SELECTORS['descripcion'])
        imagenes = tree.xpath(DEFAULT_SELECTORS['imagen'])
        logo_url = tree.xpath(DEFAULT_SELECTORS['logo'])
        logo_url = logo_url[0] if logo_url else None

        # Mostrar los datos en la consola
        self.stdout.write("Productos encontrados:")
        for i, producto in enumerate(productos):
            nombre_producto = producto.text_content().strip()
            precio_producto = precios[i].strip() if i < len(precios) else 'No disponible'
            descripcion_producto = descripciones[i].text_content().strip() if i < len(descripciones) else 'No disponible'
            imagen_url = imagenes[i] if i < len(imagenes) else 'No disponible'

            self.stdout.write(f"- Nombre: {nombre_producto}")
            self.stdout.write(f"  Precio: {precio_producto}")
            self.stdout.write(f"  Descripción: {descripcion_producto}")
            self.stdout.write(f"  Imagen: {imagen_url}")

        if logo_url:
            self.stdout.write(f"Logo URL: {logo_url}")
