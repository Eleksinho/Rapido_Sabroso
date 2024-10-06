from django.urls import path
from .views import *

urlpatterns = [
    path('', vista1, name="vista1"),
    path('menu', menu, name="menu"),
    path('logout/', logout_view, name='logout'),
    path('promotions/', menu_index, name='promotions'),
    path('menus/', menu_view, name='menu_view'),
    path('marca/<str:marca>/', productos_por_marca, name='marca'),
]

