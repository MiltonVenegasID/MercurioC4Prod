from django.utils import timezone
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
import random

class HomeView(LoginView):
    for_class = AuthenticationForm
    def get(self, request):
        form = AuthenticationForm()
        reset_form = ResetPasswordForm()
        create_form = CustomUserCreationForm()
        return render(request, 'home.html', {'login_form': form, 'reset_form': reset_form, 'create_form': create_form})
    
    def post(self, request):
        print(request.POST)
        login_form = AuthenticationForm
        register_form = CustomUserCreationForm
        context = {
            'login_form': login_form(),
            'create_form': register_form()
        }
        
        if 'login_submit' in request.POST:
            auth_form = login_form(request, data=request.POST)
            if auth_form.is_valid():
                username = auth_form.cleaned_data.get('username')
                password = auth_form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password)
                context = {
                    "success": True,
                    "message": "Inicio de sesion exitoso"
                } 
                if user is not None:
                    login(request, user)
                    return HttpResponse("Logged in successfully")
                else:
                    context = {
                        "success": False,
                        "message": "Usuario o contraseña incorrectos"
                    }
                    return JsonResponse(context)
            else:
                context = {
                    "success": False,
                    "message": "Formulario de inicio de sesion no valido"
                }
                return JsonResponse(context) 
            
        elif 'register_submit' in request.POST:
            create_form = register_form(request.POST)
            if create_form.is_valid():
                
                code = ''.join([str(random.randint(0, 9)) for _ in range(8)])
                correo = create_form.cleaned_data.get('Correo')
                cuenta = create_form.cleaned_data.get('Cuenta')
                today = timezone.now()
                
                print(hub_register(correo, cuenta))
                
                """ if hub_register(correo, cuenta) is True:
                    if not HolderUser.objects.filter(correo=correo).exists():
                        new_holder = HolderUser.objects.create(
                            correo=correo,
                            cuenta=cuenta,
                            code=code,
                            fhRegistro=today
                        )
                        new_holder.save()
                        context = {
                            "success": True,
                            "message": "Registro exitoso, por favor revise su correo para activar su cuenta"
                        }
                        return JsonResponse(context)
                    else:
                        context = {
                            "success": False,
                            "message": "Ya existe un usuario registrado con este correo"
                        }
                        return JsonResponse(context)
                else:
                    context = {
                        "success": False,
                        "message": "Los datos que ingresaste no coinciden con ningun registro en el hub, por favor verifica los datos ingresados"
                    }
                    return JsonResponse(context) """
            else:
                context = {
                    "success": False,
                    "message": "Formulario de registro no valido"
                }
                return JsonResponse(context)