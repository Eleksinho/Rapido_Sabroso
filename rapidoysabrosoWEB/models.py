from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
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
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('pagada', 'Pagada'),
        ('cancelada', 'Cancelada'),
    ]

    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='pendiente')


class OrdenProducto(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.cantidad * self.producto.precio
    
class Profile(models.Model):
    USER_LEVEL_CHOICES = (
        ('usuario', 'Usuario'),
        ('moderador', 'Moderador'),
        ('administrador', 'Administrador'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    
    # Agregamos el nuevo campo para los niveles de usuario
    user_level = models.CharField(
        max_length=13,
        choices=USER_LEVEL_CHOICES,
        default='usuario',  # Nivel predeterminado
    )

    def __str__(self):
        return f'{self.user.username} - {self.user_level}'
    
# En tu models.py

class HistorialPrecio(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  # Relación con el producto
    precio = models.CharField(max_length=50)  # Precio scrapeado
    fecha = models.DateField(auto_now_add=True)  # Fecha de scraping
    @property
    def precio_float(self):
        """Convierte el precio en CharField a un número flotante."""
        try:
            # Elimina el símbolo '$' y las comas antes de convertirlo
            return float(self.precio.replace('$', '').replace(',', ''))
        except ValueError:
            return None

    def __str__(self):
        return f"{self.producto.nombre} - {self.precio} ({self.fecha})"
    
    # SECCION MAPA Y DIRECCIONES

class Url_Locales(models.Model):
    url = models.URLField(unique=True, verbose_name="URL de la Tienda")
    
    def __str__(self):
        return self.url

class SelectorMAPA(models.Model):
    url = models.ForeignKey(Url_Locales, on_delete=models.CASCADE, related_name="selectors")
    local_selector = models.CharField(max_length=255, verbose_name="Selector CSS para el Local")
    direccion_selector = models.CharField(max_length=255, verbose_name="Selector CSS para la Dirección")
    
    def __str__(self):
        return f"Selectores para {self.url}"
    
class Mapa_data(models.Model):
    local = models.CharField(max_length=255, verbose_name="Nombre del Local")
    direccion = models.CharField(max_length=255, verbose_name="Dirección")
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")  # Nuevo campo
    coordenadas = models.CharField(max_length=255, blank=True, null=True, verbose_name="Coordenadas (Latitud, Longitud)")
    Marca = models.ForeignKey(Marca, on_delete=models.CASCADE, related_name="scraped_data")
    fuente_url_mapa = models.ForeignKey(Url_Locales, on_delete=models.CASCADE, related_name="scraped_data")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Scraping")

    def __str__(self):
        return f"{self.local} - {self.direccion}"
