from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import Usuario


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        correo = request.POST.get('correo', '').strip()
        password = request.POST.get('password', '')

        usuario = authenticate(request, correo=correo, password=password)

        if usuario is not None:
            login(request, usuario)
            messages.success(request, f'Bienvenido, {usuario.nombre} {usuario.apellido}.')
            return redirect('dashboard')

        messages.error(request, 'Credenciales inválidas o usuario inactivo.')

    return render(request, 'usuarios/login.html')


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente.')
    return redirect('login')


@login_required(login_url='login')
def dashboard_view(request):
    if not request.user.tiene_rol('ADMIN', 'CLIENTE', 'ENTRENADOR', 'NUTRICIONISTA', 'FISIOTERAPEUTA'):
        logout(request)
        messages.error(request, 'No tienes permisos para acceder a esta sección.')
        return redirect('login')

    contexto = {
        'usuario': request.user,
        'rol': request.user.rol,
    }
    return render(request, 'usuarios/dashboard.html', contexto)
