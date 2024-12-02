from django.contrib import admin
from .models import Url, Producto, PageSelector, Categoria, Marca, Profile, HistorialPrecio, Orden, OrdenProducto

# Admin para el modelo Url
@admin.register(Url)
class UrlAdmin(admin.ModelAdmin):
    list_display = ('url', 'last_scraped')
    search_fields = ('url',)

# Admin para el modelo Producto
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'marca')
    search_fields = ('nombre', 'marca__nombre')

# Admin para el modelo Marca
@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'logo_url')  # Mostrar el nombre y el logo_url
    search_fields = ('nombre',)

# Admin para el modelo PageSelector
@admin.register(PageSelector)
class PageSelectorAdmin(admin.ModelAdmin):
    list_display = ('url', 'product_selector', 'price_selector', 'description_selector', 'image_selector')
    search_fields = ('url__url',)

# Admin para el modelo Categoria
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)  # Asegúrate de incluir la coma (,) para definirlo como tupla
    search_fields = ('nombre',)

# Admin para el modelo Profile
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_level', 'bio', 'location', 'birth_date')  # Campos que deseas mostrar en la lista
    search_fields = ('user__username', 'user__email')  # Campos para buscar

@admin.register(HistorialPrecio)
class HistorialPrecioAdmin(admin.ModelAdmin):
    list_display = ('producto', 'precio', 'fecha')
    list_filter = ('fecha', 'producto')
    search_fields = ('producto__nombre',)

from django.contrib import admin
from .models import Url_Locales, SelectorMAPA, Mapa_data

@admin.register(Url_Locales)
class UrlLocalesAdmin(admin.ModelAdmin):
    list_display = ("id", "url")  # Muestra el ID y la URL en la lista
    search_fields = ("url",)  # Habilita la búsqueda por URL

@admin.register(SelectorMAPA)
class SelectorMAPAAdmin(admin.ModelAdmin):
    list_display = ("id", "url", "local_selector", "direccion_selector")  # Muestra los campos principales
    search_fields = ("url__url", "local_selector", "direccion_selector")  # Búsqueda por URL y selectores
    list_filter = ("url",)  # Filtro por la URL relacionada

@admin.register(Mapa_data)
class MapaDataAdmin(admin.ModelAdmin):
    list_display = ("id", "local", "direccion", "telefono", "coordenadas", "Marca", "fuente_url_mapa", "fecha")
    search_fields = ("local", "direccion", "telefono", "coordenadas", "Marca__nombre", "fuente_url_mapa__url")  # Búsqueda avanzada
    list_filter = ("Marca", "fuente_url_mapa", "fecha")  # Filtros por marca, fuente y fecha
    ordering = ("-fecha",)  # Orden descendente por fecha de scraping

@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha', 'total', 'estado')  # Muestra estas columnas en el listado
    list_filter = ('estado', 'fecha')  # Añade filtros por estado y fecha
    search_fields = ('id',)  # Habilita búsqueda por ID
    ordering = ('-fecha',)  # Ordena por fecha descendente

@admin.register(OrdenProducto)
class OrdenProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'orden', 'producto','user', 'cantidad', 'subtotal')  # Mostrar estos campos en el listado
    list_filter = ('orden', 'producto')  # Filtros para orden y producto
    search_fields = ('orden__id', 'producto__nombre')  # Búsqueda por ID de la orden o nombre del producto
    ordering = ('orden',)  # Ordenar por la orden

    def subtotal(self, obj):
        return obj.subtotal()
    subtotal.short_description = 'Subtotal'  # Nombre que se muestra en la columna