from django.core.management.base import BaseCommand
from rapidoysabrosoWEB.models import Url, Producto, PageSelector, Categoria, Marca, HistorialPrecio
from datetime import datetime
import requests
from lxml import html
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
from django.utils.timezone import now

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

def obtener_marca(url):
    dominio = urlparse(url).netloc
    return dominio.split('.')[1] if '.' in dominio else dominio

def categorizar_producto(nombre_producto):
    nombre_producto_lower = nombre_producto.lower()
    for categoria, palabras_clave in CATEGORIAS.items():
        if any(palabra in nombre_producto_lower for palabra in palabras_clave):
            categoria_obj, _ = Categoria.objects.get_or_create(nombre=categoria)
            return categoria_obj
    categoria_obj, _ = Categoria.objects.get_or_create(nombre='Sin Categoría')
    return categoria_obj

def descargar_imagen(url_imagen):
    try:
        response_imagen = requests.get(url_imagen)
        if response_imagen.status_code == 200:
            return response_imagen.content
        return None
    except requests.exceptions.RequestException:
        return None

# Parte del código permanece igual...

class Command(BaseCommand):
    help = 'Realiza scraping de todas las URLs almacenadas y extrae los productos'

    def handle(self, *args, **kwargs):
        urls = Url.objects.all()
        today = datetime.now().date()

        for url_obj in urls:
            # Verificar si la URL ya fue scrapeada hoy
            # if HistorialPrecio.objects.filter(producto__fuente_url=url_obj, fecha=today).exists():
            #     print(f"{url_obj.url} ya fue scrapeada hoy. Se omite.")
            #     continue  # Omitir esta URL y pasar a la siguiente

            url = url_obj.url
            print(f"Scraping {url}...")

            try:
                selectors = PageSelector.objects.get(url=url_obj)
            except PageSelector.DoesNotExist:
                print(f"No se encontraron selectores para {url}. Usando selectores por defecto.")
                selectors = None

            try:
                response = requests.get(url)
                response.raise_for_status()
            except requests.RequestException as e:
                print(f"Error al acceder a {url}: {e}")
                continue

            tree = html.fromstring(response.content)

            # Obtener productos, precios, descripciones e imágenes
            productos = tree.xpath(DEFAULT_SELECTORS['producto'])
            precios = tree.xpath(DEFAULT_SELECTORS['precio'])
            descripciones = tree.xpath(DEFAULT_SELECTORS['descripcion']) if DEFAULT_SELECTORS['descripcion'] else []
            imagenes = tree.xpath(DEFAULT_SELECTORS['imagen'])
            logo_url = tree.xpath(DEFAULT_SELECTORS['logo'])
            logo_url = logo_url[0] if logo_url else None

            if not productos or not precios:
                if selectors:
                    productos = tree.xpath(selectors.product_selector)
                    precios = tree.xpath(selectors.price_selector)
                    descripciones = tree.xpath(selectors.description_selector) if selectors.description_selector else []
                    imagenes = tree.xpath(selectors.image_selector) if selectors.image_selector else []
                    logo_url = tree.xpath(selectors.logo_selector) if selectors.logo_selector else logo_url

            if selectors is None and productos and precios:
                PageSelector.objects.create(
                    url=url_obj,
                    product_selector=DEFAULT_SELECTORS['producto'],
                    price_selector=DEFAULT_SELECTORS['precio'],
                    description_selector=DEFAULT_SELECTORS['descripcion'],
                    image_selector=DEFAULT_SELECTORS['imagen'],
                    logo_selector=DEFAULT_SELECTORS['logo']
                )

            with ThreadPoolExecutor() as executor:
                imagenes_binarias = list(executor.map(
                    descargar_imagen, 
                    [requests.compat.urljoin(url, img) if not img.startswith('http') else img for img in imagenes]
                ))

            # Procesar la marca
            marca_nombre = obtener_marca(url)
            marca, created = Marca.objects.get_or_create(nombre=marca_nombre)

            if logo_url and created:
                marca.logo_url = logo_url
                marca.save()
            elif logo_url and not marca.logo_url:
                marca.logo_url = logo_url
                marca.save()

            # Procesar cada producto
            for i, producto in enumerate(productos):
                nombre_producto = producto.text_content().strip()
                precio_producto = precios[i].strip() if i < len(precios) else None
                descripcion_producto = descripciones[i].text_content().strip() if i < len(descripciones) else None
                imagen_binaria = imagenes_binarias[i] if i < len(imagenes_binarias) else None
                imagen_url = imagenes[i] if i < len(imagenes) else None

                categoria = categorizar_producto(nombre_producto)

                # Verificar si el producto ya existe
                producto_existente = Producto.objects.filter(nombre=nombre_producto, fuente_url=url_obj).first()

                if producto_existente:
                    # Verificar si el precio ya está registrado hoy
                    historial_hoy = HistorialPrecio.objects.filter(producto=producto_existente, fecha=today).first()

                    if not historial_hoy:
                        HistorialPrecio.objects.create(producto=producto_existente, precio=precio_producto)
                    
                        if producto_existente.precio != precio_producto:
                            producto_existente.precio = precio_producto  # Actualizamos el precio del producto
                            producto_existente.descripcion = descripcion_producto
                            producto_existente.imagen_url = imagen_url
                            producto_existente.categoria = categoria
                            producto_existente.marca = marca
                            producto_existente.save(force_update=True)  # Guardamos el producto con los nuevos datos
                else:
                    # Crear un nuevo producto y agregarlo al historial
                    nuevo_producto = Producto.objects.create(
                        nombre=nombre_producto,
                        precio=precio_producto,
                        descripcion=descripcion_producto,
                        imagen_url=imagen_url,
                        fuente_url=url_obj,
                        categoria=categoria,
                        marca=marca
                    )
                    HistorialPrecio.objects.create(producto=nuevo_producto, precio=precio_producto)

            # Actualizar la fecha de última vez que se hizo scraping para la URL
            url_obj.last_scraped = now()
            url_obj.save()