from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Paciente
from .forms import PacienteForm

@login_required
def dashboard(request):
    paciente, _ = Paciente.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil de paciente actualizado.")
            return redirect("pacientes:dashboard")
    else:
        form = PacienteForm(instance=paciente)
    return render(request, "pacientes/dashboard.html", {"form": form})
