from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test

# Decorador para verificar si el usuario es moderador
def user_is_moderator(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.groups.filter(name='moderador').exists() or request.user.groups.filter(name='administrador').exists():
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('No tienes permiso para acceder a esta página.')
    return wrapper_func

# Decorador para verificar si el usuario es administrador
def user_is_admin(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.groups.filter(name='administrador').exists():
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('No tienes permiso para acceder a esta página.')
    return wrapper_func

def user_is_staff(function=None):
    # Usamos user_passes_test para verificar si el usuario tiene is_staff en True
    return user_passes_test(lambda u: u.is_staff)(function)