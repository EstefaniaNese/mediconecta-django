from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Reserva, HistorialMedico, Cobro, EstadoReserva
from .forms import ReservaForm, HistorialMedicoForm, CobroForm
from pacientes.models import Paciente
from medicos.models import Medico

@login_required
def reserva_crear(request):
    if request.method == "POST":
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            paciente, _ = Paciente.objects.get_or_create(user=request.user)
            reserva.paciente = paciente
            reserva.save()
            
            # Crear cobro automáticamente
            Cobro.objects.create(reserva=reserva, monto=0)
            
            messages.success(request, "Reserva creada con éxito.")
            return redirect('citas:reserva_lista')
    else:
        form = ReservaForm()
    
    return render(request, 'citas/reserva_form.html', {
        'form': form,
        'title': 'Nueva Reserva'
    })

@login_required
def reserva_lista(request):
    if hasattr(request.user, 'paciente'):
        reservas = Reserva.objects.filter(paciente=request.user.paciente)
    elif hasattr(request.user, 'medico'):
        reservas = Reserva.objects.filter(medico=request.user.medico)
    else:
        reservas = Reserva.objects.none()
    
    return render(request, 'citas/reserva_lista.html', {
        'reservas': reservas
    })

@login_required
def reserva_detalle(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    
    # Verificar que el usuario sea el paciente o el médico de la reserva
    if not (hasattr(request.user, 'paciente') and request.user.paciente == reserva.paciente) and \
       not (hasattr(request.user, 'medico') and request.user.medico == reserva.medico):
        messages.error(request, "No tienes permiso para ver esta reserva.")
        return redirect('citas:reserva_lista')
    
    historial = HistorialMedico.objects.filter(reserva=reserva).first()
    cobro = Cobro.objects.filter(reserva=reserva).first()
    
    return render(request, 'citas/reserva_detalle.html', {
        'reserva': reserva,
        'historial': historial,
        'cobro': cobro
    })

@login_required
def reserva_cancelar(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    
    # Verificar que el usuario sea el paciente de la reserva
    if not hasattr(request.user, 'paciente') or request.user.paciente != reserva.paciente:
        messages.error(request, "No tienes permiso para cancelar esta reserva.")
        return redirect('citas:reserva_lista')
    
    if not reserva.puede_cancelar():
        messages.error(request, "No se puede cancelar esta reserva.")
        return redirect('citas:reserva_detalle', pk=reserva.pk)
    
    reserva.estado = EstadoReserva.CANCELADA
    reserva.save()
    messages.success(request, "Reserva cancelada con éxito.")
    
    return redirect('citas:reserva_lista')

@login_required
def historial_crear(request, reserva_pk):
    reserva = get_object_or_404(Reserva, pk=reserva_pk)
    
    # Verificar que el usuario sea el médico de la reserva
    if not hasattr(request.user, 'medico') or request.user.medico != reserva.medico:
        messages.error(request, "No tienes permiso para crear un historial médico.")
        return redirect('citas:reserva_lista')
    
    if request.method == "POST":
        form = HistorialMedicoForm(request.POST)
        if form.is_valid():
            historial = form.save(commit=False)
            historial.paciente = reserva.paciente
            historial.medico = reserva.medico
            historial.reserva = reserva
            historial.save()
            
            # Actualizar estado de la reserva
            reserva.estado = EstadoReserva.COMPLETADA
            reserva.save()
            
            messages.success(request, "Historial médico creado con éxito.")
            return redirect('citas:reserva_detalle', pk=reserva.pk)
    else:
        form = HistorialMedicoForm()
    
    return render(request, 'citas/historial_form.html', {
        'form': form,
        'reserva': reserva
    })

@login_required
def cobro_actualizar(request, reserva_pk):
    reserva = get_object_or_404(Reserva, pk=reserva_pk)
    cobro = get_object_or_404(Cobro, reserva=reserva)
    
    # Verificar que el usuario sea el médico de la reserva
    if not hasattr(request.user, 'medico') or request.user.medico != reserva.medico:
        messages.error(request, "No tienes permiso para actualizar el cobro.")
        return redirect('citas:reserva_lista')
    
    if request.method == "POST":
        form = CobroForm(request.POST, instance=cobro)
        if form.is_valid():
            form.save()
            messages.success(request, "Cobro actualizado con éxito.")
            return redirect('citas:reserva_detalle', pk=reserva.pk)
    else:
        form = CobroForm(instance=cobro)
    
    return render(request, 'citas/cobro_form.html', {
        'form': form,
        'reserva': reserva
    })

@login_required
def cobro_pagar(request, reserva_pk):
    reserva = get_object_or_404(Reserva, pk=reserva_pk)
    cobro = get_object_or_404(Cobro, reserva=reserva)
    
    # Verificar que el usuario sea el paciente de la reserva
    if not hasattr(request.user, 'paciente') or request.user.paciente != reserva.paciente:
        messages.error(request, "No tienes permiso para pagar este cobro.")
        return redirect('citas:reserva_lista')
    
    if cobro.pagado:
        messages.info(request, "Este cobro ya ha sido pagado.")
        return redirect('citas:reserva_detalle', pk=reserva.pk)
    
    # Simulación de pago
    cobro.marcar_como_pagado("Tarjeta de crédito")
    messages.success(request, "Pago realizado con éxito.")
    
    return redirect('citas:reserva_detalle', pk=reserva.pk)