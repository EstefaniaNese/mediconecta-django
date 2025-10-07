from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q
from datetime import date
from .models import Paciente
from .serializers import PacienteSerializer, PacienteListSerializer

class PacienteViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar pacientes.
    """
    queryset = Paciente.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PacienteListSerializer
        return PacienteSerializer
    
    def get_queryset(self):
        queryset = Paciente.objects.select_related('user')
        
        # Filtros opcionales
        search = self.request.query_params.get('search', None)
        grupo_sanguineo = self.request.query_params.get('grupo_sanguineo', None)
        edad_min = self.request.query_params.get('edad_min', None)
        edad_max = self.request.query_params.get('edad_max', None)
        
        if search:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(user__username__icontains=search) |
                Q(rut__icontains=search) |
                Q(telefono__icontains=search)
            )
        
        if grupo_sanguineo:
            queryset = queryset.filter(grupo_sanguineo__icontains=grupo_sanguineo)
        
        if edad_min or edad_max:
            today = date.today()
            if edad_min:
                # Fecha máxima de nacimiento para tener al menos edad_min años
                max_birth_date = date(today.year - int(edad_min), today.month, today.day)
                queryset = queryset.filter(fecha_nacimiento__lte=max_birth_date)
            
            if edad_max:
                # Fecha mínima de nacimiento para tener como máximo edad_max años
                min_birth_date = date(today.year - int(edad_max) - 1, today.month, today.day)
                queryset = queryset.filter(fecha_nacimiento__gte=min_birth_date)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        """
        Endpoint para obtener estadísticas de pacientes
        """
        total_pacientes = self.get_queryset().count()
        
        # Estadísticas por grupo sanguíneo
        grupos_sanguineos = {}
        for paciente in self.get_queryset():
            grupo = paciente.grupo_sanguineo or 'No especificado'
            grupos_sanguineos[grupo] = grupos_sanguineos.get(grupo, 0) + 1
        
        # Pacientes con alergias
        pacientes_con_alergias = self.get_queryset().exclude(alergias='').count()
        
        # Pacientes por rango de edad
        hoy = date.today()
        menores_18 = 0
        entre_18_65 = 0
        mayores_65 = 0
        
        for paciente in self.get_queryset():
            if paciente.fecha_nacimiento:
                edad = hoy.year - paciente.fecha_nacimiento.year - ((hoy.month, hoy.day) < (paciente.fecha_nacimiento.month, paciente.fecha_nacimiento.day))
                if edad < 18:
                    menores_18 += 1
                elif edad <= 65:
                    entre_18_65 += 1
                else:
                    mayores_65 += 1
        
        return Response({
            'total_pacientes': total_pacientes,
            'grupos_sanguineos': grupos_sanguineos,
            'pacientes_con_alergias': pacientes_con_alergias,
            'distribucion_edad': {
                'menores_18': menores_18,
                'entre_18_65': entre_18_65,
                'mayores_65': mayores_65
            }
        })
    
    @action(detail=False, methods=['get'])
    def con_alergias(self, request):
        """
        Endpoint para obtener pacientes que tienen alergias registradas
        """
        pacientes_con_alergias = self.get_queryset().exclude(
            Q(alergias='') | Q(alergias__isnull=True)
        )
        serializer = PacienteListSerializer(pacientes_con_alergias, many=True)
        return Response({
            'total': pacientes_con_alergias.count(),
            'pacientes': serializer.data
        })
    
    @action(detail=True, methods=['get'])
    def historial_medico(self, request, pk=None):
        """
        Endpoint para obtener información médica detallada de un paciente
        """
        paciente = self.get_object()
        serializer = PacienteSerializer(paciente)
        
        return Response({
            'paciente': serializer.data,
            'notas': 'Este endpoint puede expandirse para incluir historial médico completo'
        })
