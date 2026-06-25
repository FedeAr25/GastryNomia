from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group


def bienvenido_context(request):
    if request.user.is_authenticated:
        mensaje = _(f"Bienvenido, {request.user.username}!")
    else:
        mensaje = _(
            "Inicia sesión para poder crear recetas y obtener los beneficios de nuestra web."
        )
    return {"mensaje_bienvenida": mensaje}


def user_groups(request):
    if request.user.is_authenticated:
        user_groups_list = list(request.user.groups.values_list("name", flat=True))
    else:
        user_groups_list = []

    return {
        "user_groups": user_groups_list,
    }
