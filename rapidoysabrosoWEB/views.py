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


def TiendaNueva(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        if url:
            url_instance, created = Url.objects.get_or_create(url=url)
            if created:
                # Ejecutar comando para el scraping
                call_command('scrape_urls')
                messages.success(request, "La URL fue registrada y se inició el scraping.")
                return redirect('RegistroTienda')  # Cambia por la vista deseada
            else:
                messages.info(request, "Esta URL ya está registrada.")
                return redirect('RegistroTienda')  # O la misma vista
        else:
            messages.error(request, "Por favor, ingrese una URL válida.")
            return redirect('RegistroTienda')  # O la misma vista
    return render(request, 'service/RegistroTienda.html')


    

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
            'imagen_url': 'Error',
            'descripcion': 'Error'
        }

    tree = html.fromstring(response.content)

    # Función para intentar obtener un valor de un selector y manejar errores
    def get_value(selector, xpath):
        try:
            result = tree.xpath(xpath)
            if result:
                return result[0].text_content().strip() if isinstance(result[0], html.HtmlElement) else result[0].strip()
            return 'No disponible'
        except Exception as e:
            print(f"Error al procesar selector {xpath}: {e}")
            return 'Error'

    # Extraer datos utilizando los selectores con manejo de errores
    producto = get_value(selector, product_selector)
    precio = get_value(selector, price_selector)
    descripcion = get_value(selector, description_selector)
    imagen = get_value(selector, image_selector)

    # Imprimir los resultados intermedios para depuración
    data = {
        'nombre': producto,
        'precio': precio,
        'imagen_url': imagen,
        'descripcion': descripcion,
    }
    
    # Procesar y devolver los resultados
    return data


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


#carrito---------------------------------------
from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from .utils import agregar_al_carrito, eliminar_del_carrito, obtener_carrito

def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    productos = []
    total = 0

    for producto_id, datos in carrito.items():
        producto = get_object_or_404(Producto, id=producto_id)
        cantidad = datos.get('cantidad', 1)
        precio_listo = int(datos.get('precio'))

        total += precio_listo * cantidad  # Accumulate total properly # Sumamos el precio * cantidad al total
        productos.append({
            'producto': producto,
            'cantidad': cantidad,
            'total': precio_listo * cantidad,  
        })
    

    
    return render(request, 'service/carrito.html', {'productos': productos, 'total': total})



def agregar_a_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    producto = get_object_or_404(Producto, id=producto_id)

     # Precio en centavos

    producto_id = str(producto_id)  # ID como cadena
    precio_listo = producto.precio.replace('$', '').replace('.', '')  # Eliminar símbolo y separadores

    if producto_id in carrito:
        carrito[producto_id]['cantidad'] += 1
    else:
        carrito[producto_id] = {
            'nombre': producto.nombre,
            'precio': precio_listo,  # Precio en centavos
            'cantidad': 1,
            'imagen_url': producto.imagen_url,
        }
    print(precio_listo)
    request.session['carrito'] = carrito
    return redirect('ver_carrito')







def eliminar_de_carrito(request, producto_id):
    """Elimina un producto del carrito almacenado en la sesión."""
    carrito = request.session.get('carrito', {})

    # Eliminar el producto del carrito
    if str(producto_id) in carrito:
        del carrito[str(producto_id)]
        request.session['carrito'] = carrito  # Actualiza la sesión

    return redirect('ver_carrito')


#Integracion--------------------------------------------------------------

from django.shortcuts import get_object_or_404, redirect
from transbank.webpay.webpay_plus.transaction import Transaction
from .models import Producto, Orden, OrdenProducto
def iniciar_orden(request):
    carrito = request.session.get('carrito', {})
    if not carrito:
        return redirect('ver_carrito')

    orden = Orden.objects.create(total=0)
    total = 0

    for producto_id, datos in carrito.items():
        producto = get_object_or_404(Producto, id=producto_id)
        cantidad = datos.get('cantidad',0)
        precio_listo = int(datos.get('precio',0))
        total += precio_listo * cantidad 
        OrdenProducto.objects.create(orden=orden, producto=producto, cantidad=cantidad)
        
    orden.total = total 
    orden.save()

    transaction = Transaction()
    response = transaction.create(
        buy_order=str(orden.id),
        session_id=str(request.user.id if request.user.is_authenticated else 'anon'),
        amount=total,  # Total en centavos
        return_url=request.build_absolute_uri('/webpay/confirmar/')
    )

    request.session['webpay_token'] = response['token']
    return redirect(response['url'] + '?token_ws=' + response['token'])



def confirmar_pago(request):
    token = request.GET.get('token_ws')
    transaction = Transaction()
    response = transaction.commit(token)

    if response['status'] == 'AUTHORIZED':
        orden_id = response['buy_order']
        orden = Orden.objects.get(id=orden_id)
        orden.estado = 'pagada'
        orden.save()

        # Limpiar el carrito
        request.session.pop('carrito', None)

        return render(request, 'service/confirmacion.html', {'orden': orden})
    else:
        return render(request, 'error_pago.html', {'response': response})
