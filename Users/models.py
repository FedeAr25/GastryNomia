from django.db import models
from django.contrib.auth.models import AbstractUser


class UsuarioPersonalizado(AbstractUser):
    telefono = models.CharField(max_length=20, null=True, blank=True)
    dni = models.CharField(max_length=20, null=True, blank=True)
    foto_perfil = models.ImageField(upload_to="user_fp/", null=True, blank=True)

    def __str__(self):
        return f"{self.username} - {self.dni}"
