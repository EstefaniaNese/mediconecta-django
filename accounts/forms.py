from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .validators import (
    validate_password_length,
    validate_password_digit,
    validate_password_uppercase,
    validate_password_special_char
)

class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu contraseña'
        }),
        validators=[
            validate_password_length,
            validate_password_digit,
            validate_password_uppercase,
            validate_password_special_char
        ],
        help_text="La contraseña debe tener al menos 8 caracteres, incluir una letra mayúscula, un número y un carácter especial."
    )
    password2 = forms.CharField(
        label="Repite tu contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirma tu contraseña'
        })
    )

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Elige un nombre de usuario'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'tu@email.com'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tu nombre'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tu apellido'
            }),
        }

    def clean(self):
        data = super().clean()
        if data.get("password") != data.get("password2"):
            raise forms.ValidationError("Las contraseñas no coinciden")
        return data

class CustomLoginForm(forms.Form):
    """
    Formulario personalizado de login sin validaciones de email
    """
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu nombre de usuario'
        }),
        label='Nombre de usuario',
        help_text='Ingresa el nombre de usuario con el que te registraste'
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu contraseña'
        }),
        label='Contraseña'
    )
    
    def clean(self):
        """Validación personalizada sin validaciones de email"""
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        
        if not username:
            raise forms.ValidationError({'username': ['Este campo es obligatorio.']})
        
        if not password:
            raise forms.ValidationError({'password': ['Este campo es obligatorio.']})
        
        return cleaned_data
