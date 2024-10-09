from django.contrib.auth.decorators import login_required  # Decorador para requerir inicio de sesión
from django.views.decorators.csrf import csrf_exempt  # Decorador para permitir solicitudes POST sin CSRF
from django.contrib.auth import authenticate, login, logout  # Funciones para autenticar y manejar sesiones de usuario
from django.db import IntegrityError  # Manejo de errores de integridad en la base de datos
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse  # Respuestas HTTP
from django.shortcuts import render, get_object_or_404  # Funciones para renderizar vistas y obtener objetos
from django.urls import reverse  # Función para generar URLs
import json  # Módulo para manejar JSON
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage # Crear páginas en el front
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models import User

""" Main page """
def index(request):
    return render(request, "mundoalado/index.html")


def login_view(request):
    if request.method == "POST":
        # Intentar iniciar sesión
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Verificar si la autenticación fue exitosa
        if user is not None:
            login(request, user)
            return render(request, "mundoalado/index.html")  # Redirigir al índice
        else:
            return render(request, "mundoalado/login.html", {
                "message": "Invalid username and/or password."  # Mensaje de error
            })
    else:
        return render(request, "mundoalado/login.html")  # Renderizar la vista de inicio de sesión


def logout_view(request):
    logout(request)  # Cerrar sesión
    return render(request, "mundoalado/index.html")  # Redirigir al índice


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Asegurarse de que la contraseña coincide con la confirmación
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "mundoalado/register.html", {
                "message": "Passwords must match."  # Mensaje de error
            })

        if not username or not email or not password or not confirmation:
            return render(request, "mundoalado/register.html", {
                "message": "You have to complete all the fields."
            })
        # Intentar crear un nuevo usuario
        try:
            user = User.objects.create_user(username, email, password)
            user.save()  # Guardar el usuario en la base de datos
        except IntegrityError:
            return render(request, "mundoalado/register.html", {
                "message": "Username already taken."  # Mensaje de error
            })
        login(request, user)  # Iniciar sesión con el nuevo usuario
        return render(request, "mundoalado/index.html")  # Redirigir al índice
    else:
        return render(request, "mundoalado/register.html")  # Renderizar la vista de registro