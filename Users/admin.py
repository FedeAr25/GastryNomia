from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UsuarioPersonalizado


@admin.register(UsuarioPersonalizado)
class UsuarioPersonalizadoAdmin(UserAdmin):
    list_display = ['username', 'email', 'dni', 'telefono', 'is_active', 'is_staff', 'get_grupos']
    list_filter  = ['is_active', 'is_staff', 'groups']
    search_fields = ['username', 'email', 'dni']

    fieldsets = UserAdmin.fieldsets + (
        ('Datos adicionales', {'fields': ('telefono', 'dni', 'foto_perfil')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Datos adicionales', {'fields': ('telefono', 'dni', 'foto_perfil')}),
    )

    def get_grupos(self, obj):
        grupos = obj.groups.values_list('name', flat=True)
        return ', '.join(grupos) if grupos else '—'
    get_grupos.short_description = 'Grupos'
