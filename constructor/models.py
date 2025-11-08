from time import timezone
import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.contrib.postgres.fields import JSONField


class CustomUser(AbstractUser):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="El numero celular debe de tener un formato de solo numeros y por lo menos 9 digitos: Se permiten hasta 15 digitos")
    Telefono = models.CharField(max_length=50)
    TipoUsuario = models.CharField(max_length=50)
    Suscripciones = models.JSONField(default=dict)
    Estado = models.BooleanField(default=True)
    ref = models.CharField(max_length=100, null=True, blank=True)
    
class HolderUser(models.Model):
    cuenta = models.CharField(max_length=100)
    correo = models.EmailField(blank=False, null=False)
    fhRegistro = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=100, null=True, blank=True)
    
class ClientesGC(models.Model):
    Nombre = models.CharField(max_length=100)
    Estatus = models.BooleanField(default=True)
    Cta = models.CharField(null=True) 
    
    def __str__(self):
        return f"{self.Cta} - {self.Nombre}" 
    
class GestoresCreationRequest(models.Model):
    email = models.EmailField(unique=True)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_used = models.BooleanField(default=False)
    
    def is_expired(self):
        return (timezone.now() - self.created_at).days <= 1