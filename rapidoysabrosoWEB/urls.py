from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', login_view, name="login"),
    path('menu', menu, name="menu"),
    path('logout/', logout_view, name='logout'),
    path('marca/<int:marca>/', productos_por_marca, name='marca'), # Cambia str por int para el ID
    path('categoria/<str:categoria>/', categorias, name='categoria'),
    path('producto/<int:id>/', producto, name='producto'),
    path('register/', register, name='register'),
    path('RegistroTienda/', TiendaNueva, name='RegistroTienda'),
    path('TiendaSelector',TiendaSelector, name='TiendaSelector'),
    path('SelectorTienda/<int:selector_id>', SelectorTienda, name='SelectorTienda'),
    path('profile/', profile_view, name='profile'),
    path('mapa_locales/', mapa_locales, name='mapa_locales'),
    path('MostrarHistorial/', MostrarHistorial, name='MostrarHistorial'),

#Carrito-----------------------------------------------------

path('agregar_a_carrito/<int:producto_id>//', agregar_a_carrito, name='agregar_a_carrito'),
path('eliminar_de_carrito/<int:producto_id>/', eliminar_de_carrito, name='eliminar_de_carrito'),
path('ver_carrito/', ver_carrito, name='ver_carrito'),




#Integracion-------------------------------------------------
   path('orden/iniciar/', views.iniciar_orden, name='iniciar_orden'),
    path('webpay/confirmar/', views.confirmar_pago, name='confirmar_pago'),
]