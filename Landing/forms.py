from django import forms
from django.forms import inlineformset_factory
from .models import Receta, Ingrediente, PasoInstruccion

_INPUT = 'w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-orange-400 focus:border-transparent'
_INPUT_ICON = _INPUT + ' pl-10'


class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = ['nombre', 'imagen', 'tiempo', 'porciones', 'dificultad', 'categorias', 'etiquetas', 'notas']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': _INPUT,
                'placeholder': 'Ej: Tarta de manzana vegana',
            }),
            'tiempo': forms.TextInput(attrs={
                'class': _INPUT_ICON,
                'placeholder': '30 min',
            }),
            'porciones': forms.NumberInput(attrs={
                'class': _INPUT_ICON,
                'placeholder': '4',
            }),
            'dificultad': forms.Select(attrs={
                'class': 'w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-orange-400',
            }),
            'categorias': forms.CheckboxSelectMultiple(),
            'notas': forms.Textarea(attrs={
                'class': 'w-full p-3 border border-gray-300 rounded-md h-24',
                'placeholder': '¿Algún consejo, variante o información nutricional que quieras compartir?',
            }),
        }


class IngredienteForm(forms.ModelForm):
    class Meta:
        model = Ingrediente
        fields = ['descripcion']
        widgets = {
            'descripcion': forms.TextInput(attrs={
                'class': 'flex-1 p-2 border border-gray-300 rounded-md w-full',
                'placeholder': 'Ej: 2 tazas de harina',
            }),
        }


class PasoForm(forms.ModelForm):
    class Meta:
        model = PasoInstruccion
        fields = ['descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={
                'class': 'flex-1 p-2 border border-gray-300 rounded-md h-20 w-full',
                'placeholder': 'Describe este paso de la receta',
            }),
        }


IngredienteFormSet = inlineformset_factory(
    Receta, Ingrediente,
    form=IngredienteForm,
    extra=3,
    can_delete=True,
)

PasoFormSet = inlineformset_factory(
    Receta, PasoInstruccion,
    form=PasoForm,
    extra=2,
    can_delete=True,
)
