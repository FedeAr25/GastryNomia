from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UsuarioPersonalizado


class UsuarioPersonalizadoForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UsuarioPersonalizado
        fields = UserCreationForm.Meta.fields + ("telefono", "dni", "foto_perfil")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].help_text = "minimo 8 caracteres"


class UsuarioAuthenticationForm(AuthenticationForm):
    class Meta:
        model = UsuarioPersonalizado
        fields = ("username", "password")
