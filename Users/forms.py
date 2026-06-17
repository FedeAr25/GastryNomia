from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UsuarioPersonalizado


class UsuarioPersonalizadoForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UsuarioPersonalizado
        fields = UserCreationForm.Meta.fields + ("telefono", "dni", "foto_perfil")

        input_styles = "w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition duration-200"

        widgets = {
            "username": forms.TextInput(
                attrs={"class": input_styles, "placeholder": "Ej. chef_fede"}
            ),
            "email": forms.EmailInput(
                attrs={"class": input_styles, "placeholder": "correo@gastrynomia.com"}
            ),
            # ¡AQUÍ ESTÁ EL TRUCO! Django los llama password1 y password2
            "password1": forms.PasswordInput(
                attrs={"class": input_styles, "placeholder": "Contraseña"}
            ),
            "password2": forms.PasswordInput(
                attrs={"class": input_styles, "placeholder": "Repite tu contraseña"}
            ),
        }
