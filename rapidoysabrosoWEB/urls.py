from django.urls import path
from .views import *

urlpatterns = [
    path('', login_view, name="vista1"),
    path('menu', menu, name="menu"),
    path('logout/', logout_view, name='logout'),
    path('marca/<int:marca>/', productos_por_marca, name='marca'), # Cambia str por int para el ID
    path('categoria/<str:categoria>/', categorias, name='categoria'),
    path('producto/<int:id>/', producto, name='producto'),
    path('agregar_a_orden/<int:producto_id>/', agregar_a_orden, name='agregar_a_orden'),
    path('orden/', ver_orden, name='ver_orden'),
    path('eliminar_de_orden/<int:producto_id>/', eliminar_de_orden, name='eliminar_de_orden'),
    path('register/', register, name='register'),
    path('RegistroTienda/', TiendaNueva, name='RegistroTienda'),
    path('TiendaSelector',TiendaSelector, name='TiendaSelector'),
    path('SelectorTienda/<int:selector_id>', SelectorTienda, name='SelectorTienda'),
    path('profile/', profile_view, name='profile'),
]