from django.shortcuts import render, redirect , get_object_or_404
from django.urls import path, include
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core.management import call_command
from django.db import connection
from threading import Thread

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Profile

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .Forms import ProfileForm


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile
from .Forms import ProfileForm, SelectorForm

@login_required
def profile_view(request):
    # Obtén el perfil del usuario actual
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        # Crea un formulario para el perfil con los datos del POST
        form = ProfileForm(request.POST, instance=profile)
        
        if form.is_valid():
            # Guarda los cambios en el perfil
            form.save()  

            # Actualiza el usuario
            user = request.user
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.set_password(request.POST.get('password'))  # Actualiza la contraseña si se proporciona
            user.save()  # Guarda los cambios en el usuario
            
            return redirect('profile')  # Redirige al perfil después de guardar
    else:
        form = ProfileForm(instance=profile)  # Carga el perfil existente en el formulario

    return render(request, 'registration/profile.html', {'form': form})




def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Inicio de sesión exitoso.')
            return redirect('menu')  # Cambia 'menu' por la URL de redirección deseada
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
            return render(request, 'service/login.html')  # Asegúrate de que esta plantilla exista

    return render(request, 'service/login.html')

def logout_view(request):
    logout(request)
    return redirect('vista1')

def menu(request):
    # Obtén todos los productos, categorías y marcas
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()  
    marcas = Marca.objects.all()  
    
    # Obtener parámetros de la consulta
    precio_min = request.GET.get('precio_min', None)
    precio_max = request.GET.get('precio_max', None)
    sort_by = request.GET.get('sort', None)  

    # Filtrar por rango de precios si se proporciona
   

    # Contexto para la plantilla
    context = {
        'productos': productos,
        'marcas': marcas,  
        'categorias': categorias
    }

    return render(request, 'service/menu.html', context)


def productos_por_marca(request, marca):
    # Filtra los productos por el ID de la marca
    productos_filtrados = Producto.objects.filter(marca_id=marca)
    # Obtén el objeto Marca para mostrar más detalles si es necesario
    marca_obj = Marca.objects.get(id=marca)
    
    return render(request, 'service/marca.html', {'productos': productos_filtrados, 'marca': marca_obj})





def categorias(request, categoria):
    categorias = Categoria.objects.all()

    if categoria == "Todas":
        productos = Producto.objects.all()  
    else:
        
        categoria_obj = get_object_or_404(Categoria, nombre=categoria) 
        productos = Producto.objects.filter(categoria=categoria_obj) 

    context = {
        'productos': productos,
        'categoria_seleccionada': categoria,
        'categorias': categorias 
    }
    return render(request, 'service/categoria.html', context)

def producto(request, id):
    categorias = Categoria.objects.all()
    producto = get_object_or_404(Producto, id=id)
    context = {
        'producto': producto,
        'categorias': categorias 
    }
    return render(request, 'service/producto.html', context )






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
            return redirect(' service/vista1')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})



def TiendaNueva(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        if url:
            url_instance, created = Url.objects.get_or_create(url=url)
            if created:
                # Ejecuta el scraping en un hilo para evitar bloquear la vista
                thread = Thread(target=ejecutar_scraping)
                thread.start()
                return redirect('menu')  
            else:
                return HttpResponse("Esta URL ya está registrada.")
        else:
            return HttpResponse("Por favor, ingrese una URL válida.")
    else:
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



def ejecutar_scraping():
    try:
        call_command('scrape_urls')
        connection.close() 
        pass 
    except Exception as e:
        print(f"Error en el scraping: {e}")

from django.db import transaction

def SelectorTienda(request, selector_id):
    selector = get_object_or_404(PageSelector, id=selector_id)

    if request.method == 'POST':
        with transaction.atomic():
            form = SelectorForm(request.POST, instance=selector)
            if form.is_valid():
                form.save()
                thread = Thread(target=ejecutar_scraping)
                thread.start()
                return redirect('TiendaSelector')
    else:
        form = SelectorForm(instance=selector)

    context = {
        'form': form,
        'selector': selector
    }
    return render(request, 'service/SelectorTienda.html', context)
