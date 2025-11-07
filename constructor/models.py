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
    