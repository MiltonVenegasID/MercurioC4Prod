from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout, authenticate
import requests
import json
from .forms import *
from .functions import *
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

@csrf_exempt
def testing_comms(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            return JsonResponse({'status': 'sueccess', 'message': 'Data received successfully'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
    
def get_csrf_token(request):
    token = get_token(request)
    return JsonResponse({'csrfToken': token})
    

@csrf_exempt
def home_view(request):
    login_form = AuthenticationForm
    register_form = CustomUserCreationForm

    if 'login_submit' in request.POST:
        auth_form = login_form(request, data=request.POST)
        if auth_form.is_valid():
            username = auth_form.cleaned_data.get('username')
            password = auth_form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({
                    "success": True,
                    "message": "Inicio de sesion exitoso"
                })
            else:
                return JsonResponse({
                    "success": False,
                    "message": "Usuario o contraseña incorrectos"
                })
        else:
            errors = json.loads(auth_form.errors.as_json())
            message = errors.get("__all__", [{}])[0].get("message", "Usuario o contraseña incorrectos")
            return JsonResponse({
                "success": False,
                "message": message
            })

    elif 'register_submit' in request.POST:
        create_form = register_form(request.POST)
        if create_form.is_valid():
            nombre = create_form.cleaned_data.get('Nombre')
            cta = create_form.cleaned_data.get('Cta')
            response = hub_register(nombre, cta)
            if response['success']:
                return JsonResponse({
                    "success": True,
                    "message": "Registro exitoso, por favor revise su correo para continuar con el proceso."
                })
            else:
                return JsonResponse({
                    "success": False,
                    "message": response['message']
                })
        else:
            return JsonResponse({
                "success": False,
                "message": "Formulario de registro no valido"
            })

    return JsonResponse({
        "success": False,
        "message": "Acción no reconocida"
    }, status=400)
