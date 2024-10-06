from django.db import models

# Modelo para almacenar las URLs que se van a scrapear
class Url(models.Model):
    url = models.URLField(unique=True)  # URL que vas a scrapear
    last_scraped = models.DateTimeField(null=True, blank=True)  # Fecha de la última vez que fue scrapeada

    def __str__(self):
        return self.url

# Modelo para las categorías de los productos
class Categoria(models.Model):
    nombre = models.CharField(max_length=255, unique=True)  # Nombre de la categoría, única para evitar duplicados

    def __str__(self):
        return self.nombre

# Modelo para los productos
class Producto(models.Model):
    nombre = models.CharField(max_length=255)  # Nombre del producto
    precio = models.CharField(max_length=50)  # Precio del producto
    descripcion = models.TextField(null=True, blank=True)  # Descripción del producto
    imagen_url = models.URLField(null=True, blank=True)  # URL de la imagen
    imagen = models.BinaryField(null=True, blank=True)  # Almacena el contenido de la imagen en binario
    fuente_url = models.ForeignKey(Url, on_delete=models.CASCADE)  # Relación con la URL desde la que se extrajo
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)  # Relación con la categoría del producto
    marca = models.CharField(max_length=255, null=True, blank=True)  # Nombre de la marca extraída de la URL

    def __str__(self):
        return f"{self.nombre} ({self.marca})"

# Modelo para los selectores de scraping
class PageSelector(models.Model):
    url = models.ForeignKey(Url, on_delete=models.CASCADE)  # Relación con la URL correspondiente
    product_selector = models.CharField(max_length=255)  # Selector CSS o XPath para los productos
    price_selector = models.CharField(max_length=255)  # Selector CSS o XPath para los precios
    description_selector = models.CharField(max_length=255, null=True, blank=True)  # Selector para la descripción
    image_selector = models.CharField(max_length=255, null=True, blank=True)  # Selector para la imagen

    def __str__(self):
        return f'Selectores para {self.url}'