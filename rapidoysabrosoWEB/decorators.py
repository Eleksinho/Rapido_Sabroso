from django.http import HttpResponse
from django.shortcuts import redirect

# Decorador para verificar si el usuario es moderador
def user_is_moderator(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.profile.user_level == 'moderador' or request.user.profile.user_level == 'administrador':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('No tienes permiso para acceder a esta página.')
    return wrapper_func

# Decorador para verificar si el usuario es administrador
def user_is_admin(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.profile.user_level == 'administrador':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('No tienes permiso para acceder a esta página.')
    return wrapper_func
