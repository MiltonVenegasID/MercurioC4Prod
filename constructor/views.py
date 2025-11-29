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
from pymongo import MongoClient
from django.contrib.auth.hashers import check_password

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
    register_form = CustomUserCreationForm

    if 'login_submit' in request.POST:
        try:
            data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
            username = data.get('username')
            password = data.get('password')
            
            if not username or not password:
                return JsonResponse({
                    "success": False,
                    "message": "Usuario y contraseña son requeridos"
                })
            
            client = MongoClient('mongodb://localhost:27017/')
            db = client['GlobalDatabase']
            users_collection = db['GlobalUsers']
            
            
            user_data = users_collection.find_one({'username': username})
            
            if user_data and check_password(password, user_data.get('password')):
                request.session['user_id'] = str(user_data['_id'])
                request.session['username'] = user_data['username']
                return JsonResponse({
                    "success": True,
                    "message": "Inicio de sesión exitoso"
                })
            else:
                return JsonResponse({
                    "success": False,
                    "message": "Usuario o contraseña incorrectos"
                })
        except Exception as e:
            return JsonResponse({
                "success": False,
                "message": f"Error en el proceso de autenticación: {str(e)}"
            }, status=500)
        

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
