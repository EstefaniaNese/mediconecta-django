from django import forms
from .models import Reserva, HistorialMedico, Cobro

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['medico', 'fecha', 'hora_inicio', 'hora_fin', 'motivo']
        widgets = {
            'medico': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Selecciona un médico'
            }),
            'fecha': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'hora_inicio': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
            'hora_fin': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
            'motivo': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Describe el motivo de tu consulta'
            }),
        }
        labels = {
            'medico': 'Médico',
            'fecha': 'Fecha de la cita',
            'hora_inicio': 'Hora de inicio',
            'hora_fin': 'Hora de fin',
            'motivo': 'Motivo de la consulta',
        }
        
class HistorialMedicoForm(forms.ModelForm):
    class Meta:
        model = HistorialMedico
        fields = ['diagnostico', 'tratamiento', 'observaciones']
        widgets = {
            'diagnostico': forms.Textarea(attrs={'rows': 3}),
            'tratamiento': forms.Textarea(attrs={'rows': 3}),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }
        
class CobroForm(forms.ModelForm):
    class Meta:
        model = Cobro
        fields = ['monto']
