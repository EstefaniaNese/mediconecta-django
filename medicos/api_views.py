from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Medico, Especialidad
from .serializers import MedicoSerializer, MedicoListSerializer, EspecialidadSerializer

class MedicoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar médicos.
    """
    queryset = Medico.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return MedicoListSerializer
        return MedicoSerializer
    
    def get_queryset(self):
        queryset = Medico.objects.select_related('user', 'especialidad')
        
        # Filtros opcionales
        especialidad = self.request.query_params.get('especialidad', None)
        disponible = self.request.query_params.get('disponible', None)
        search = self.request.query_params.get('search', None)
        
        if especialidad:
            queryset = queryset.filter(especialidad__nombre__icontains=especialidad)
        
        if disponible is not None:
            queryset = queryset.filter(disponible=disponible.lower() == 'true')
        
        if search:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(user__username__icontains=search) |
                Q(especialidad__nombre__icontains=search)
            )
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def disponibles(self, request):
        """
        Endpoint para obtener solo médicos disponibles
        """
        medicos_disponibles = self.get_queryset().filter(disponible=True)
        serializer = MedicoListSerializer(medicos_disponibles, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def por_especialidad(self, request):
        """
        Endpoint para obtener médicos agrupados por especialidad
        """
        especialidades = Especialidad.objects.prefetch_related('medicos__user')
        result = []
        
        for especialidad in especialidades:
            medicos = especialidad.medicos.filter(disponible=True)
            if medicos.exists():
                medicos_data = MedicoListSerializer(medicos, many=True).data
                result.append({
                    'especialidad': especialidad.nombre,
                    'medicos': medicos_data,
                    'total_medicos': medicos.count()
                })
        
        return Response(result)

class EspecialidadViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet de solo lectura para especialidades médicas.
    """
    queryset = Especialidad.objects.all()
    serializer_class = EspecialidadSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['get'])
    def medicos(self, request, pk=None):
        """
        Endpoint para obtener todos los médicos de una especialidad específica
        """
        especialidad = self.get_object()
        medicos = especialidad.medicos.filter(disponible=True).select_related('user')
        serializer = MedicoListSerializer(medicos, many=True)
        return Response({
            'especialidad': EspecialidadSerializer(especialidad).data,
            'medicos': serializer.data,
            'total_medicos': medicos.count()
        })
