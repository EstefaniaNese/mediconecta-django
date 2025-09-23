from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
            )
            login(request, user)
            messages.success(request, "Cuenta creada correctamente.")
            return redirect("core:index")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})

@login_required
def profile(request):
    user = request.user
    if request.method == "POST":
        form = RegisterForm(request.POST, instance=user)
        if form.is_valid():
            user.username = form.cleaned_data["username"]
            user.email = form.cleaned_data["email"]
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            
            # Solo actualizar la contraseña si se proporciona
            if form.cleaned_data["password"]:
                user.set_password(form.cleaned_data["password"])
            
            user.save()
            messages.success(request, "Perfil actualizado correctamente.")
            return redirect("accounts:profile")
    else:
        form = RegisterForm(instance=user)
    
    return render(request, "accounts/profile.html", {"form": form})

@login_required
def user_delete(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        messages.success(request, "Tu cuenta ha sido eliminada.")
        return redirect("core:index")
    
    return render(request, "accounts/delete_confirm.html")
