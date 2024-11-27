from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core.management import call_command
from django.db import connection , transaction
from threading import Thread
from django.contrib import messages
from .Forms import *
from .decorators import user_is_staff
from django.utils import timezone
import json
from rest_framework.authtoken.models import Token
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)



@login_required
def profile_view(request):
    user = request.user  # Trabajamos directamente con el usuario autenticado

    if request.method == 'POST':
        # Actualizar los datos del usuario
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)

        # Guardar cambios
        try:
            with transaction.atomic():
                user.save()
                messages.success(request, "Perfil actualizado exitosamente.")
                return redirect('profile')  # Redirige a la vista de perfil
        except Exception as e:
            messages.error(request, f"Error al actualizar el perfil: {e}")

    return render(request, 'registration/profile.html', {'user': user})

from rest_framework.authtoken.models import Token
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Obtener o crear el token del usuario
            token, _ = Token.objects.get_or_create(user=user)

            # Almacenar el token en una cookie o retornarlo (para APIs, se usaría un JSON Response)
            messages.success(request, f'Inicio de sesión exitoso. Token: {token.key}')
            return redirect('menu')  # Cambia 'menu' por tu URL deseada
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
            return render(request, 'service/login.html')

    return render(request, 'service/login.html')

def logout_view(request):
    if request.user.is_authenticated:
        try:
            # Eliminar el token asociado al usuario
            token = Token.objects.get(user=request.user)
            token.delete()
        except Token.DoesNotExist:
            pass  # Si no hay token, no hacemos nada

    logout(request)
    messages.success(request, "Has cerrado sesión exitosamente.")
    return redirect('login')

    # Agregar un mensaje de éxito
    messages.success(request, "Has cerrado sesión exitosamente.")

    # Redirigir a la página de inicio o cualquier otra página
    return redirect('login')


def obtener_productos_con_precio_bajo():
    # Obtiene la fecha actual
    fecha_actual = timezone.now().date()

    # Lista para almacenar productos cuyo precio actual es menor que el anterior
    productos_con_precio_bajo = []

    # Iterar sobre todos los productos
    for producto in Producto.objects.all():
        # Obtener los historiales de precio ordenados por fecha, para cada producto
        historial_precio = HistorialPrecio.objects.filter(producto=producto).order_by('fecha')

        if historial_precio.count() > 1:
            # El primer registro de historial (el más antiguo)
            primer_precio = historial_precio.first().precio_float

            # El último registro de historial (el más reciente)
            ultimo_precio = historial_precio.last().precio_float

            # Compara si el precio actual (último precio) es menor que el primero
            if ultimo_precio < primer_precio:
                productos_con_precio_bajo.append(producto)
                
    return productos_con_precio_bajo

def menu(request):
    fecha_actual = timezone.localtime(timezone.now()).date()
    productos_creados_hoy = Producto.objects.filter(
        historialprecio__fecha=fecha_actual
    ).distinct()

    producto_bajo = obtener_productos_con_precio_bajo()
    categorias = Categoria.objects.all()  
    marcas = Marca.objects.all()  
    context = {
        'bajaron' : producto_bajo,
        'productos': productos_creados_hoy,
        'marcas': marcas,  
        'categorias': categorias
    }

    return render(request, 'service/menu.html', context)







def productos_por_marca(request, marca):
    # Obtiene la fecha actual ajustada a la zona horaria configurada en TIME_ZONE
    fecha_actual = timezone.localtime(timezone.now()).date()  # Solo la fecha sin la hora
    
    # Filtra los productos por la marca y con un historial de precios registrado hoy (fecha actual)
    productos_filtrados = Producto.objects.filter(
        marca_id=marca,
        historialprecio__fecha=fecha_actual  # Filtra por la fecha actual
    ).distinct()  # Distinct para evitar duplicados si hay varios registros del mismo día
    
    # Obtiene el objeto Marca para mostrar más detalles
    marca_obj = Marca.objects.get(id=marca)
    
    # Renderiza la plantilla con el contexto
    return render(request, 'service/marca.html', {
        'productos': productos_filtrados,
        'marca': marca_obj
    })

def categorias(request, categoria):
    # Obtiene la fecha actual ajustada a la zona horaria configurada en TIME_ZONE
    fecha_actual = timezone.localtime(timezone.now()).date()  # Solo la fecha sin la hora
    
    # Obtiene todas las categorías para la navegación
    categorias = Categoria.objects.all()

    if categoria == "Todas":
        # Filtra los productos que tienen un historial de precios registrado hoy
        productos = Producto.objects.filter(
            historialprecio__fecha=fecha_actual  # Filtra por la fecha actual
        ).distinct()  # Distinct para evitar duplicados si hay varios registros del mismo día
    else:
        # Obtiene la categoría seleccionada
        categoria_obj = get_object_or_404(Categoria, nombre=categoria)
        
        # Filtra los productos por la categoría y con un historial de precios registrado hoy
        productos = Producto.objects.filter(
            categoria=categoria_obj,
            historialprecio__fecha=fecha_actual  # Filtra por la fecha actual
        ).distinct()

    # Contexto para la plantilla
    context = {
        'productos': productos,
        'categoria_seleccionada': categoria,
        'categorias': categorias
    }
    
    # Renderiza la plantilla
    return render(request, 'service/categoria.html', context)

def producto(request, id):
    categorias = Categoria.objects.all()
    producto = get_object_or_404(Producto, id=id)

    # Obtiene los registros del historial de precios
    historial_precios = HistorialPrecio.objects.filter(producto=producto).order_by('fecha')

    # Serializa los datos a formato JSON
    fechas = [historial.fecha.strftime('%Y-%m-%d') for historial in historial_precios]  # Convierte a string
    precios = [convertir_precio(historial.precio) for historial in historial_precios]

    # Verifica los datos antes de pasarlos al contexto
    print('Fechas:', fechas)  # Imprimir fechas
    print('Precios:', precios)  # Imprimir precios

    context = {
        'producto': producto,
        'categorias': categorias,
        'fechas': json.dumps(fechas),  # Convertir a JSON
        'precios': json.dumps(precios),  # Convertir precios a JSON
    }
    return render(request, 'service/producto.html', context)


def convertir_precio(precio):
    """Convierte el precio de CharField a float eliminando caracteres no numéricos."""
    return float(precio.replace('$', '').replace('.', '').replace(',', ''))

def agregar_a_orden(request, producto_id):
    
    orden, creada = Orden.objects.get_or_create(id=request.session.get('orden_id'))

    # Guardamos la id de la orden en la sesión
    request.session['orden_id'] = orden.id

    # Obtenemos el producto por su ID
    producto = get_object_or_404(Producto, id=producto_id)

    # Agregamos el producto a la orden o aumentamos la cantidad si ya está
    orden_producto, creado = OrdenProducto.objects.get_or_create(orden=orden, producto=producto)
    if not creado:
        orden_producto.cantidad += 1
    orden_producto.save()

    # Calcular el total de la orden, realizando la conversión en una línea
    total = sum(float(item.producto.precio.replace('$', '').replace('.', '').replace(',', '.')) * int(item.cantidad) for item in orden.ordenproducto_set.all())
    
    # Guardar el total en la orden
    orden.total = total
    orden.save()

    return redirect('ver_orden')


def eliminar_de_orden(request, producto_id):
    orden_id = request.session.get('orden_id')
    if orden_id:
        orden = get_object_or_404(Orden, id=orden_id)
        orden_producto = orden.ordenproducto_set.filter(producto__id=producto_id).first()
        
        if orden_producto:
            orden_producto.delete()
            
            # Recalcular el total
            total = sum(float(item.producto.precio.replace('$', '').replace('.', '').replace(',', '.')) * item.cantidad for item in orden.ordenproducto_set.all())
            orden.total = total
            orden.save()

    return redirect('ver_orden')




def ver_orden(request):
    orden = Orden.objects.get(id=request.session.get('orden_id'))
    productos_en_orden = orden.ordenproducto_set.all()
    return render(request, 'service/orden.html', {'orden': orden, 'productos_en_orden': productos_en_orden})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(' service/login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})




# @user_is_staff
# def TiendaNueva(request):
#     if request.method == 'POST':
#         url = request.POST.get('url')
#         if url:
#             url_instance, created = Url.objects.get_or_create(url=url)
#             if created:
#                 # Llama al comando de Django para ejecutar el scraping          
#                 call_command('scrape_urls')
#             else:
#                 return HttpResponse("Esta URL ya está registrada.")
#         else:
#             return HttpResponse("Por favor, ingrese una URL válida.")
#     else:
#         return render(request, 'service/RegistroTienda.html')

@user_is_staff
def TiendaNueva(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        if url:
            url_instance, created = Url.objects.get_or_create(url=url)
            if created:
                # Ejecutar comando para el scraping
                call_command('scrape_urls')
                messages.success(request, "La URL fue registrada y se inició el scraping.")
                return redirect('RegistroTIenda')  # Cambia por la vista deseada
            else:
                messages.info(request, "Esta URL ya está registrada.")
                return redirect('RegistroTienda')  # O la misma vista
        else:
            messages.error(request, "Por favor, ingrese una URL válida.")
            return redirect('RegistroTienda')  # O la misma vista
    return render(request, 'service/RegistroTienda.html')


    
@user_is_staff
def TiendaSelector(request):
    # Obtener todas las URLs y sus selectores
    urls = Url.objects.all()  # Obtén todas las URLs
    selectores = PageSelector.objects.all()  # Obtener todos los selectores

    context = {
        'urls': urls,
        'selectores': selectores
    }
    return render(request, 'service/TiendaSelector.html', context)




import requests
from lxml import html

def scrape_view(selector):
    # Obtener la URL desde el selector
    url = selector.url.url  # Asegúrate de acceder a la URL correcta
    print(f"URL para scraping: {url}")  # Verifica que obtienes la URL correcta

    product_selector = selector.product_selector
    price_selector = selector.price_selector
    description_selector = selector.description_selector
    image_selector = selector.image_selector

    # Realiza la solicitud y el scraping
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error al acceder a la URL: {url} con el código de estado {response.status_code}")
        return {
            'nombre': 'Error',
            'precio': 'Error',
            'imagen_url': 'Error'
        }
    
    tree = html.fromstring(response.content)

    # Extraer datos usando los selectores del formulario
    producto = tree.xpath(product_selector)
    precio = tree.xpath(price_selector)
    descripcion = tree.xpath(description_selector)
    imagen = tree.xpath(image_selector)

    # Imprimir los resultados intermedios para depuración
   
    data = {
        'nombre': producto[0].text_content().strip() if producto else 'No disponible',
        'precio': precio[0].strip() if precio else 'No disponible',
        'imagen_url': imagen[0] if imagen else 'No disponible',
        'descripcion': descripcion[0].text_content().strip() if descripcion else 'No disponible',
        
        # Agrega más campos según sea necesario
    }
    
    # Procesar y devolver los resultados
    return data
@user_is_staff
def SelectorTienda(request, selector_id):
    selector = get_object_or_404(PageSelector, id=selector_id)
    producto_preview = None  # Almacenar el producto de vista previa
    scraping_iniciado = False  # Indica si se ha iniciado el scraping completo

    if request.method == 'POST':
        form = SelectorForm(request.POST, instance=selector)
        if form.is_valid():
            with transaction.atomic():
                form.save()  # Guarda los selectores actualizados

                if 'preview' in request.POST:
                    # Obtener producto de ejemplo con los selectores actuales
                    producto_preview = scrape_view(selector)
                    print(f"Producto preview: {producto_preview}")  # Depuración

                elif 'save' in request.POST:
                    # Guardar y ejecutar el scraping completo en segundo plano
                    scraping_iniciado = True
                    thread = Thread(target=lambda: call_command('scrape_urls'))
                    thread.start()                
                    print("Comando scrape_urls iniciado en segundo plano")
                    

                print("Formulario guardado y acciones ejecutadas")  # Depuración
        else:
            print("El formulario no es válido")  # Depuración
    else:
        form = SelectorForm(instance=selector)

    context = {
        'form': form,
        'selector': selector,
        'producto_preview': producto_preview,
        'scraping_iniciado': scraping_iniciado
    }
    return render(request, 'service/SelectorTienda.html', context)