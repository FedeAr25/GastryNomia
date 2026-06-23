from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UsuarioPersonalizado


class UsuarioPersonalizadoForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UsuarioPersonalizado
        fields = UserCreationForm.Meta.fields + ("telefono", "dni", "foto_perfil")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 1. Eliminar el texto de ayuda SOLO del Username:
        self.fields["username"].help_text = ""

        # 2. Eliminar el texto de ayuda SOLO de la contraseña (las reglas):
        # En los formularios de creación de Django, el primer campo de contraseña se llama 'username' o viene atado a validadores,
        # pero para quitar ese bloque gigante de texto de las contraseñas puedes vaciar estos campos que lo traen embebido:
        if "username" in self.fields:
            self.fields["username"].help_text = ""

        # Si tienes campos específicos de los que quieras borrar el texto,
        # simplemente los llamas por su nombre entre los corchetes:
        # self.fields['telefono'].help_text = ''
