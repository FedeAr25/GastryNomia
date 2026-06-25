from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UsuarioPersonalizado

input_styles = "w-full px-4 py-3 bg-gray-200 border border-gray-200 rounded-xl text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition duration-200"


class UsuarioPersonalizadoForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UsuarioPersonalizado
        fields = UserCreationForm.Meta.fields + ("telefono", "dni", "foto_perfil")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": input_styles})
        self.fields["password1"].widget.attrs.update({"class": input_styles})
        self.fields["password2"].widget.attrs.update({"class": input_styles})
        self.fields["telefono"].widget.attrs.update({"class": input_styles})
        self.fields["dni"].widget.attrs.update({"class": input_styles})
        self.fields["username"].help_text = ""
        self.fields["password1"].help_text = ""


class UsuarioAuthenticationForm(AuthenticationForm):
    class Meta:
        model = UsuarioPersonalizado
        fields = ("username", "password")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": input_styles})
        self.fields["password"].widget.attrs.update({"class": input_styles})
