from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UsuarioPersonalizadoForm


def registrarse(request):
    if request.method == "POST":
        form = UsuarioPersonalizadoForm(request.POST, request.FILES)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect("landing")
    else:
        form = UsuarioPersonalizadoForm()
    return render(request, "registration/register.html", {"form": form})
