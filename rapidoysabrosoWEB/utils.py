# utils.py

def agregar_al_carrito(request, producto_id, cantidad=1):
    """Agrega un producto al carrito de la sesión."""
    carrito = request.session.get('carrito', {})
    carrito[producto_id] = carrito.get(producto_id, 0) + cantidad
    request.session['carrito'] = carrito

def eliminar_del_carrito(request, producto_id):
    """Elimina un producto del carrito."""
    carrito = request.session.get('carrito', {})
    if producto_id in carrito:
        del carrito[producto_id]
        request.session['carrito'] = carrito

def vaciar_carrito(request):
    """Vacía el carrito."""
    request.session['carrito'] = {}


def obtener_carrito(request):
    carrito = request.session.get('carrito', {})
    for producto_id, datos in carrito.items():
        if not isinstance(datos, dict):
            # Reemplaza con un formato válido o lanza un error
            carrito[producto_id] = {'cantidad': 1, 'precio': 0}
    return carrito
