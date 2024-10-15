from django.shortcuts import render, redirect
from django.urls import path, include
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Producto,  Categoria   # Asegúrate de importar el modelo Producto

# Vista de autenticación
def vista1(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('menu') 
        else:
            error_message = 'Usuario o contraseña incorrectos.'
            return render(request, 'service/vista1.html', {'error_message': error_message})
    
    return render(request, 'service/vista1.html')

def menu(request):
    return render(request, 'service/menu.html')

def logout_view(request):
    logout(request)
    return redirect('vista1')

def menu(request):
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    marcas_unicas = Producto.objects.values_list('marca', flat=True).distinct()
    context = {
        'productos': productos,
        'marcas_unicas': marcas_unicas,
        'categorias': categorias
    }
    return render(request, 'service/menu.html', context)

    
def productos_por_marca(request, marca):
    # Filtrar los productos por la marca seleccionada
    productos_filtrados = Producto.objects.filter(marca=marca)
    return render(request, 'service/marca.html', {'productos': productos_filtrados, 'marca': marca})

from django.shortcuts import render, get_object_or_404
from .models import Producto, Categoria

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
    return render(request, 'service/producto.html', {'producto': producto})

