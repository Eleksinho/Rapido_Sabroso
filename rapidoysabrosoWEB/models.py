from django.db import models
from django.utils.text import slugify
# Modelo para almacenar las URLs que se van a scrapear
class Url(models.Model):
    url = models.URLField(unique=True)  # URL que vas a scrapear
    last_scraped = models.DateTimeField(null=True, blank=True)  # Fecha de la última vez que fue scrapeada

    def __str__(self):
        return self.url

# Modelo para las categorías de los productos
class Categoria(models.Model):
    nombre = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nombre

class Marca(models.Model):
    nombre = models.CharField(max_length=255, unique=True)  # Nombre de la marca
    logo_url = models.URLField(null=True, blank=True)  # URL del logo
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)  # Logo de la marca

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
    marca = models.ForeignKey(Marca, on_delete=models.SET_NULL, null=True, blank=True)  # Relación con la marca

    def __str__(self):
        return f"{self.nombre} ({self.marca})"

    @property
    def precio_float(self):
        """Convierte el precio en CharField a un número flotante."""
        try:
            # Elimina el símbolo '$' y las comas antes de convertirlo
            return float(self.precio.replace('$', '').replace(',', ''))
        except ValueError:
            return None

# Modelo para los selectores de scraping
class PageSelector(models.Model):
    url = models.ForeignKey(Url, on_delete=models.CASCADE)  # Relación con la URL correspondiente
    product_selector = models.CharField(max_length=255)  # Selector CSS o XPath para los productos
    price_selector = models.CharField(max_length=255)  # Selector CSS o XPath para los precios
    description_selector = models.CharField(max_length=255, null=True, blank=True)  # Selector para la descripción
    image_selector = models.CharField(max_length=255, null=True, blank=True)  # Selector para la imagen
    logo_selector = models.CharField(max_length=255, null=True, blank=True)  # Selector para el logo

    def __str__(self):
        return f'Selectores para {self.url}'
    

class Orden(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class OrdenProducto(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.cantidad * self.producto.precio