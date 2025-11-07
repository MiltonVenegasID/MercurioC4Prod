from .models import *
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.password_validation import validate_password
from django.forms import JSONField

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'Nombre', 'Apellidos', 'Correo', 'Telefono', 'TipoUsuario', 'Suscripciones', 'Estado', 'ref', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        validate_password(password2, self.instance)
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.Nombre = self.cleaned_data['Nombre']
        user.Apellidos = self.cleaned_data['Apellidos']
        user.Correo = self.cleaned_data['Correo']
        user.Telefono = self.cleaned_data['Telefono']
        user.TipoUsuario = self.cleaned_data['TipoUsuario']
        user.Suscripciones = self.cleaned_data['Suscripciones']
        user.Estado = self.cleaned_data['Estado']
        user.ref = self.cleaned_data['ref']
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class ResetPasswordForm(forms.Form):
    usernamepass = forms.CharField(
        required=True,
        label='username',
        strip=False,
        widget=forms.TextInput(attrs={'aria-label': 'Usuario', 'class': 'form-control'})
    )
    emailpass = forms.EmailField(
        required=True,
        label='email',
        widget=forms.EmailInput(attrs={'aria-label': 'Correo', 'class': 'form-control'})
    )
    
class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields['username'].label = 'Usuario'
        self.fields['password'].label = 'Contraseña'
        
    class Meta:
        model = User
        fields = ['username', 'password']
        
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                "Este usuario no esta activo",
                code='inactive',
            )
            
    def set_request(self, request):
        self.request = request