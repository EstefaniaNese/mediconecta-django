from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer personalizado para incluir información adicional del usuario
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Agregar información personalizada al token
        token['username'] = user.username
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['is_staff'] = user.is_staff
        
        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Vista personalizada para obtener tokens JWT
    """
    serializer_class = CustomTokenObtainPairSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Endpoint para registrar nuevos usuarios y obtener token automáticamente
    """
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    first_name = request.data.get('first_name', '')
    last_name = request.data.get('last_name', '')
    
    if not username or not email or not password:
        return Response({
            'error': 'Username, email y password son requeridos'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Verificar si el usuario ya existe
    if User.objects.filter(username=username).exists():
        return Response({
            'error': 'El nombre de usuario ya existe'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(email=email).exists():
        return Response({
            'error': 'El email ya está registrado'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Crear el usuario
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        # Generar tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Usuario registrado exitosamente',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_staff': user.is_staff
            },
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'error': f'Error al crear usuario: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    """
    Endpoint para cerrar sesión (invalidar token)
    """
    try:
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        
        return Response({
            'message': 'Sesión cerrada exitosamente'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': f'Error al cerrar sesión: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """
    Endpoint para obtener el perfil del usuario autenticado
    """
    user = request.user
    
    # Obtener información adicional del perfil si existe
    profile_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'is_staff': user.is_staff,
        'date_joined': user.date_joined,
        'last_login': user.last_login
    }
    
    # Agregar información específica si es médico o paciente
    try:
        if hasattr(user, 'medico'):
            medico = user.medico
            profile_data['tipo_usuario'] = 'medico'
            profile_data['especialidad'] = medico.especialidad.nombre if medico.especialidad else None
            profile_data['registro_colegio'] = medico.registro_colegio
            profile_data['disponible'] = medico.disponible
        elif hasattr(user, 'paciente'):
            paciente = user.paciente
            profile_data['tipo_usuario'] = 'paciente'
            profile_data['rut'] = paciente.rut
            profile_data['telefono'] = paciente.telefono
            profile_data['grupo_sanguineo'] = paciente.grupo_sanguineo
        else:
            profile_data['tipo_usuario'] = 'usuario_general'
    except:
        profile_data['tipo_usuario'] = 'usuario_general'
    
    return Response(profile_data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_token(request):
    """
    Endpoint para verificar si un token es válido
    """
    token = request.data.get('token')
    if not token:
        return Response({
            'error': 'Token requerido'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        from rest_framework_simplejwt.tokens import AccessToken
        access_token = AccessToken(token)
        user_id = access_token['user_id']
        user = User.objects.get(id=user_id)
        
        return Response({
            'valid': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'valid': False,
            'error': 'Token inválido'
        }, status=status.HTTP_401_UNAUTHORIZED)
