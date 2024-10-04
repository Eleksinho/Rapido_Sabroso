from django.db import models

# Create your models here.

class Url(models.Model):
    url = models.URLField(unique=True)  # URL que vas a scrapear
    last_scraped = models.DateTimeField(null=True, blank=True)  # Fecha de la última vez que fue scrapeada

    def __str__(self):
        return self.url

class Producto(models.Model):
    nombre = models.CharField(max_length=255)  # Nombre del producto
    precio = models.CharField(max_length=50)  # Precio del producto, puedes ajustar el max_length según sea necesario
    descripcion = models.TextField(null=True, blank=True)  # Descripción del producto
    imagen_url = models.URLField(null=True, blank=True)  # URL de la imagen del producto
    fuente_url = models.ForeignKey(Url, on_delete=models.CASCADE)  # Relación con la URL desde la que se extrajo

    def __str__(self):
        return self.nombre
    
class PageSelector(models.Model):
    url = models.ForeignKey(Url, on_delete=models.CASCADE)  # Relación con la URL correspondiente
    product_selector = models.CharField(max_length=255)  # Selector CSS o XPath para los productos
    price_selector = models.CharField(max_length=255)  # Selector CSS o XPath para los precios
    description_selector = models.CharField(max_length=255, null=True, blank=True)  # Selector para la descripción
    image_selector = models.CharField(max_length=255, null=True, blank=True)  # Selector para la imagen

    def __str__(self):
        return f'Selectores para {self.url}'

