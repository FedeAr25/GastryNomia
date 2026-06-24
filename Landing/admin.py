from django.contrib import admin
from .models import Categoria, Etiqueta, Receta, Ingrediente, PasoInstruccion


class IngredienteInline(admin.TabularInline):
    model = Ingrediente
    extra = 1


class PasoInline(admin.TabularInline):
    model = PasoInstruccion
    extra = 1


@admin.register(Receta)
class RecetaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'autor', 'dificultad', 'porciones', 'fecha_creacion']
    list_filter = ['dificultad', 'categorias']
    search_fields = ['nombre', 'autor__username']
    inlines = [IngredienteInline, PasoInline]


admin.site.register(Categoria)
admin.site.register(Etiqueta)
