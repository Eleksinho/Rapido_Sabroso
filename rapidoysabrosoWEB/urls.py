from django.urls import path
from .views import *

urlpatterns = [
    path('', vista1, name="vista1"),
    path('menu', menu, name="menu"),
    path('logout/', logout_view, name='logout'),
    path('marca/<str:marca>/', productos_por_marca, name='marca'),
    path('categoria/<str:categoria>/', categorias, name='categoria'),
    path('producto/<int:id>/', producto, name='producto'),
    path('agregar_a_orden/<int:producto_id>/', agregar_a_orden, name='agregar_a_orden'),
    path('orden/', ver_orden, name='ver_orden'),
    path('eliminar_de_orden/<int:producto_id>/', eliminar_de_orden, name='eliminar_de_orden'),

    
]

