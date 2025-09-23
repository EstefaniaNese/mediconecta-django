from django import forms
from .models import Medico, Especialidad

class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ["especialidad", "registro_colegio", "telefono", "horario_inicio", "horario_fin", "disponible"]
        widgets = {
            'horario_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'horario_fin': forms.TimeInput(attrs={'type': 'time'}),
        }