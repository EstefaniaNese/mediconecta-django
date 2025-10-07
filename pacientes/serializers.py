from rest_framework import serializers
from .models import Paciente
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class PacienteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Paciente
        fields = [
            'id', 'user', 'rut', 'telefono', 'fecha_nacimiento', 
            'direccion', 'grupo_sanguineo', 'alergias'
        ]
        read_only_fields = ['id']

class PacienteListSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.CharField(source='user.get_full_name', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    edad = serializers.SerializerMethodField()
    
    class Meta:
        model = Paciente
        fields = [
            'id', 'nombre_completo', 'email', 'rut', 'telefono', 
            'fecha_nacimiento', 'edad', 'grupo_sanguineo'
        ]
    
    def get_edad(self, obj):
        if obj.fecha_nacimiento:
            from datetime import date
            today = date.today()
            return today.year - obj.fecha_nacimiento.year - ((today.month, today.day) < (obj.fecha_nacimiento.month, obj.fecha_nacimiento.day))
        return None
