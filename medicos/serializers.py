from rest_framework import serializers
from .models import Medico, Especialidad
from django.contrib.auth.models import User

class EspecialidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidad
        fields = ['id', 'nombre', 'descripcion']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

class MedicoSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    especialidad = EspecialidadSerializer(read_only=True)
    especialidad_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Medico
        fields = [
            'id', 'user', 'especialidad', 'especialidad_id', 
            'registro_colegio', 'telefono', 'horario_inicio', 
            'horario_fin', 'disponible'
        ]
        read_only_fields = ['id']

class MedicoListSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.CharField(source='user.get_full_name', read_only=True)
    especialidad_nombre = serializers.CharField(source='especialidad.nombre', read_only=True)
    
    class Meta:
        model = Medico
        fields = [
            'id', 'nombre_completo', 'especialidad_nombre', 
            'registro_colegio', 'telefono', 'disponible'
        ]
