from django.core.management.base import BaseCommand
from rapidoysabrosoWEB.models import Url, Producto, PageSelector
import requests
from lxml import html
from datetime import datetime

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
            imagenes = tree.xpath(selectors.image_selector) if selectors.image_selector else []

            # Validar que se hayan encontrado datos
            if not productos or not precios:
                self.stdout.write(self.style.ERROR(f"No se encontraron productos o precios en {url}"))
                continue

            # Guardar los productos extraídos en la base de datos
            for i, producto in enumerate(productos):
                nombre_producto = producto.text_content().strip()
                precio_producto = precios[i].strip() if i < len(precios) else None
                descripcion_producto = descripciones[i].text_content().strip() if i < len(descripciones) else None
                
                # Asegurarse de que 'imagenes[i]' sea un elemento de imagen antes de obtener el 'src'
                imagen_url = imagenes[i].get('src') if i < len(imagenes) and isinstance(imagenes[i], html.HtmlElement) else None

                # Verificar si el producto ya existe en la base de datos
                producto_existente = Producto.objects.filter(nombre=nombre_producto).first()

                if producto_existente:
                    # Actualizar el producto existente
                    producto_existente.precio = precio_producto
                    producto_existente.descripcion = descripcion_producto
                    producto_existente.imagen_url = imagen_url
                    producto_existente.fuente_url = url_obj
                    producto_existente.save()
                    self.stdout.write(self.style.SUCCESS(f"Producto '{nombre_producto}' actualizado con éxito."))
                else:
                    # Crear una nueva entrada en la tabla de productos
                    Producto.objects.create(
                        nombre=nombre_producto,
                        precio=precio_producto,
                        descripcion=descripcion_producto,
                        imagen_url=imagen_url,
                        fuente_url=url_obj
                    )
                    self.stdout.write(self.style.SUCCESS(f"Producto '{nombre_producto}' guardado con éxito."))

            # Actualizar la fecha de última vez scrapeada
            url_obj.last_scraped = datetime.now()
            url_obj.save()
