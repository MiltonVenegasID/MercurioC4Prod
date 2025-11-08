from .models import *
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.password_validation import validate_password
from django.forms import JSONField

User = get_user_model()

#I will generate here the stand for users before passing to user model instead
class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = ClientesGC
        fields = ['Nombre', 'Cta']
        widgets = {
            'Nombre': forms.TextInput(),
            'Cta': forms.TextInput(),
        }
        labels = {
            'Nombre': 'Razon social',
            'Cta': 'Cuenta Global'
        }
    
    def save(self, commit=True):
        cliente = super().save(commit=False)
        cliente.Razon = self.cleaned_data['Nombre']
        cliente.Cta = self.cleaned_data['Cta']
        if commit:
            cliente.save()
        return cliente
    
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