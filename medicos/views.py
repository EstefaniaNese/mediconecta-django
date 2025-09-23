from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Medico
from .forms import MedicoForm

@login_required
def dashboard(request):
    medico, _ = Medico.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = MedicoForm(request.POST, instance=medico)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil de médico actualizado.")
            return redirect("medicos:dashboard")
    else:
        form = MedicoForm(instance=medico)
    return render(request, "medicos/dashboard.html", {"form": form})
