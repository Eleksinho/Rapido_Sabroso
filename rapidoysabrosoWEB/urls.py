from django.urls import path , include
from .views import vista1, vistaBk,mcdonals




urlpatterns = [
    path('', vista1,name="vista1"),
    path('vistaBk/', vistaBk,name="vistaBk"),
    path('mcdonals/', mcdonals,name="mcdonals")
 ]