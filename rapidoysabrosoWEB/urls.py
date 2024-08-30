from django.urls import path , include
from .views import vista1
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', vista1,name="vista1")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)