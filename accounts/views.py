from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.views import View
from django.urls import reverse_lazy
from .forms import RegisterForm, CustomLoginForm

class CustomLoginView(View):
    """
    Vista personalizada de login con mensajes de éxito y error
    """
    template_name = 'accounts/login.html'
    form_class = CustomLoginForm
    
    def get(self, request):
        """Muestra el formulario de login"""
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        """Procesa el formulario de login"""
        form = self.form_class(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Autenticar usuario
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(
                    request, 
                    f'¡Bienvenido/a, {username}! Has iniciado sesión exitosamente.'
                )
                return redirect('core:index')
            else:
                messages.error(
                    request,
                    'Credenciales incorrectas. Por favor, verifica tu nombre de usuario y contraseña.'
                )
        else:
            # Solo mostrar errores de campos obligatorios, no de email
            for field, errors in form.errors.items():
                if field == 'username' and any('correo' in str(error).lower() or 'email' in str(error).lower() for error in errors):
                    form.errors[field] = ['Este campo es obligatorio.']
        
        return render(request, self.template_name, {'form': form})

class CustomLogoutView(LogoutView):
    """
    Vista personalizada de logout con mensaje de confirmación
    """
    next_page = reverse_lazy('accounts:login')
    
    def dispatch(self, request, *args, **kwargs):
        """Maneja el logout con mensaje"""
        username = request.user.username if request.user.is_authenticated else 'Usuario'
        messages.info(
            request,
            f'Has cerrado sesión exitosamente. ¡Hasta luego, {username}!'
        )
        return super().dispatch(request, *args, **kwargs)

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
            messages.success(request, f"¡Cuenta creada exitosamente! Bienvenido/a, {user.username}.")
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
