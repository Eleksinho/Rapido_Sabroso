from django.contrib import admin
from .models import Url, Producto, PageSelector, Categoria, Marca, Profile

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
