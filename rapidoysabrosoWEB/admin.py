from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Url, Producto, PageSelector

@admin.register(Url)
class UrlAdmin(admin.ModelAdmin):
    list_display = ('url', 'last_scraped')
    search_fields = ('url',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'fuente_url')
    search_fields = ('nombre', 'fuente_url__url')

@admin.register(PageSelector)
class PageSelectorAdmin(admin.ModelAdmin):
    list_display = ('url', 'product_selector', 'price_selector', 'description_selector', 'image_selector')
    search_fields = ('url__url',)
