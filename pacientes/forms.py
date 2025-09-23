from django import forms
from .models import Paciente

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ["rut", "telefono", "fecha_nacimiento", "direccion", "grupo_sanguineo", "alergias"]
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'alergias': forms.Textarea(attrs={'rows': 3}),
        }