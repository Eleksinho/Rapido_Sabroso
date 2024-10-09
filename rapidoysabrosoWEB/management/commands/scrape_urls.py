from django.core.management.base import BaseCommand
from rapidoysabrosoWEB.models import Url, Producto, PageSelector, Categoria
import requests
from lxml import html
from urllib.parse import urlparse
from datetime import datetime
import os
from django.conf import settings

# Definir las palabras clave para cada categoría
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

def obtener_marca(url):
    # Extraer la marca del dominio
    dominio = urlparse(url).netloc
    marca = dominio.split('.')[1]  # Extraer la parte que está entre los puntos
    return marca

def categorizar_producto(nombre_producto):
    nombre_producto_lower = nombre_producto.lower()  # Convertir el nombre a minúsculas para hacer la búsqueda insensible a mayúsculas/minúsculas
    
    # Verificar cada categoría y sus palabras clave
    for categoria, palabras_clave in CATEGORIAS.items():
        if any(palabra in nombre_producto_lower for palabra in palabras_clave):
            categoria_obj, created = Categoria.objects.get_or_create(nombre=categoria)
            return categoria_obj

    # Si no coincide con ninguna palabra clave, asignar 'Sin Categoría'
    categoria_obj, created = Categoria.objects.get_or_create(nombre='Sin Categoría')
    return categoria_obj

class Command(BaseCommand):
    help = 'Realiza scraping de todas las URLs almacenadas y extrae los productos'

    def handle(self, *args, **kwargs):
        # Obtener todas las URLs para scraping
        urls = Url.objects.all()

        for url_obj in urls:
            url = url_obj.url
            self.stdout.write(f"Scraping {url}...")

            # Obtener los selectores correspondientes para esa URL
            try:
                selectors = PageSelector.objects.get(url=url_obj)
            except PageSelector.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"No se encontraron selectores para {url}"))
                continue

            # Hacer la solicitud GET a la URL
            response = requests.get(url)
            if response.status_code != 200:
                self.stdout.write(self.style.ERROR(f"Error al acceder a {url}"))
                continue

            # Parsear el contenido HTML
            tree = html.fromstring(response.content)

            # Extraer los datos usando los selectores de la base de datos
            productos = tree.xpath(selectors.product_selector)
            precios = tree.xpath(selectors.price_selector)
            descripciones = tree.xpath(selectors.description_selector) if selectors.description_selector else []
            imagenes = tree.xpath(selectors.image_selector)  # Usamos el nuevo selector aquí

            # Obtener la marca desde la URL
            marca = obtener_marca(url)

            # Validar que se hayan encontrado datos
            if not productos or not precios:
                self.stdout.write(self.style.ERROR(f"No se encontraron productos o precios en {url}"))
                continue

            # Guardar los productos extraídos en la base de datos
            for i, producto in enumerate(productos):
                nombre_producto = producto.text_content().strip()
                precio_producto = precios[i].strip() if i < len(precios) else None
                descripcion_producto = descripciones[i].text_content().strip() if i < len(descripciones) else None
                imagen_url = imagenes[i] if i < len(imagenes) else None  # Ahora 'imagenes' tiene las URLs directamente

                # Categorizar el producto según su nombre
                categoria = categorizar_producto(nombre_producto)

                # Verificar si la imagen_url es relativa y corregirla si es necesario
                if imagen_url:
                    # Si la URL es relativa, convertirla a absoluta
                    if not imagen_url.startswith('http'):
                        imagen_url = requests.compat.urljoin(url, imagen_url)

                # Descargar la imagen dentro del ciclo
                imagen_binaria = None
                if imagen_url:
                    try:
                        # Descargar la imagen
                        response_imagen = requests.get(imagen_url)
                        if response_imagen.status_code == 200:
                            # Almacenar el contenido de la imagen en binario
                            imagen_binaria = response_imagen.content
                        else:
                            self.stdout.write(self.style.ERROR(f"Error al descargar la imagen desde {imagen_url}: {response_imagen.status_code}"))
                    except requests.exceptions.RequestException as e:
                        self.stdout.write(self.style.ERROR(f"Error al descargar la imagen: {e}"))

                # Verificar si el producto ya existe en la base de datos (nombre + fuente_url)
                producto_existente = Producto.objects.filter(nombre=nombre_producto, fuente_url=url_obj).first()

                if producto_existente:
                    # Si ya existe, actualizar los datos
                    producto_existente.precio = precio_producto
                    producto_existente.descripcion = descripcion_producto
                    producto_existente.imagen_url = imagen_url  # Usar la URL de la imagen
                    producto_existente.imagen = imagen_binaria  # Usar el contenido binario de la imagen
                    producto_existente.categoria = categoria
                    producto_existente.marca = marca
                    producto_existente.save()
                    self.stdout.write(self.style.SUCCESS(f"Producto '{nombre_producto}' actualizado con éxito."))
                else:
                    # Crear una nueva entrada en la tabla de productos
                    Producto.objects.create(
                        nombre=nombre_producto,
                        precio=precio_producto,
                        descripcion=descripcion_producto,
                        imagen_url=imagen_url,  # Guardar la URL de la imagen
                        imagen=imagen_binaria,  # Guardar el contenido binario de la imagen
                        fuente_url=url_obj,
                        categoria=categoria,
                        marca=marca
                    )
                    self.stdout.write(self.style.SUCCESS(f"Producto '{nombre_producto}' guardado con éxito."))

            # Actualizar la fecha de última vez scrapeada
            url_obj.last_scraped = datetime.now()
            url_obj.save()