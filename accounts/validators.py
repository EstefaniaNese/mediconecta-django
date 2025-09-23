import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

def validate_password_length(password):
    """Valida que la contraseña tenga al menos 8 caracteres."""
    if len(password) < 8:
        raise ValidationError(
            _("La contraseña debe tener al menos 8 caracteres."),
            code='password_too_short',
        )

def validate_password_digit(password):
    """Valida que la contraseña contenga al menos un dígito."""
    if not any(char.isdigit() for char in password):
        raise ValidationError(
            _("La contraseña debe contener al menos un número."),
            code='password_no_digit',
        )

def validate_password_uppercase(password):
    """Valida que la contraseña contenga al menos una letra mayúscula."""
    if not any(char.isupper() for char in password):
        raise ValidationError(
            _("La contraseña debe contener al menos una letra mayúscula."),
            code='password_no_upper',
        )

def validate_password_special_char(password):
    """Valida que la contraseña contenga al menos un carácter especial."""
    special_chars = r"[!@#$%^&*(),.?\":{}|<>]"
    if not re.search(special_chars, password):
        raise ValidationError(
            _("La contraseña debe contener al menos un carácter especial (!@#$%^&*(),.?\":{}|<>)."),
            code='password_no_special',
        )
