from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm

def contact_form(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Gracias! Te responderemos pronto.")
            return redirect("contacto:form")
    else:
        form = ContactForm()
    return render(request, "contacto/form.html", {"form": form})
