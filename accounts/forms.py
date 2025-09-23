from django import forms
from django.contrib.auth.models import User
from .validators import (
    validate_password_length,
    validate_password_digit,
    validate_password_uppercase,
    validate_password_special_char
)

class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        validators=[
            validate_password_length,
            validate_password_digit,
            validate_password_uppercase,
            validate_password_special_char
        ],
        help_text="La contraseña debe tener al menos 8 caracteres, incluir una letra mayúscula, un número y un carácter especial."
    )
    password2 = forms.CharField(label="Repite tu contraseña", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]

    def clean(self):
        data = super().clean()
        if data.get("password") != data.get("password2"):
            raise forms.ValidationError("Las contraseñas no coinciden")
        return data
