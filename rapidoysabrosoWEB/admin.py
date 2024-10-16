from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Url, Producto, PageSelector , Categoria

@admin.register(Url)
class UrlAdmin(admin.ModelAdmin):
    list_display = ('url', 'last_scraped')
    search_fields = ('url',)

from django.contrib import admin
from .models import Producto, Marca

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'marca')
    search_fields = ('nombre', 'marca__nombre')

@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'logo')


@admin.register(PageSelector)
class PageSelectorAdmin(admin.ModelAdmin):
    list_display = ('url', 'product_selector', 'price_selector', 'description_selector', 'image_selector')
    search_fields = ('url__url',)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    # Corregir 'list_display' y 'search_fields' como tuplas
    list_display = ('nombre',)  # Asegúrate de incluir la coma (,) para definirlo como tupla
    search_fields = ('nombre',)