from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RecetaForm, IngredienteFormSet, PasoFormSet
from .models import Etiqueta, Receta


def landing(request):
    return render(request, "landing/landing.html")


def about(request):
    return render(request, "landing/about.html")


def challenges(request):
    return render(request, "landing/challenges.html")




def explorar(request):
    recetas = Receta.objects.select_related('autor').prefetch_related('etiquetas', 'categorias').order_by('-fecha_creacion')

    q = request.GET.get('q', '').strip()
    dificultad = request.GET.get('dificultad', '')

    if q:
        recetas = recetas.filter(nombre__icontains=q)
    if dificultad:
        recetas = recetas.filter(dificultad=dificultad)

    return render(request, 'landing/explorar.html', {
        'recetas': recetas,
        'q': q,
        'dificultad': dificultad,
        'dificultad_choices': Receta.DIFICULTAD_CHOICES,
    })


@login_required
def recipes(request):
    if request.method == 'POST':
        form = RecetaForm(request.POST, request.FILES)
        ingrediente_formset = IngredienteFormSet(request.POST, prefix='ingredientes')
        paso_formset = PasoFormSet(request.POST, prefix='pasos')

        if form.is_valid() and ingrediente_formset.is_valid() and paso_formset.is_valid():
            receta = form.save(commit=False)
            receta.autor = request.user
            receta.save()
            form.save_m2m()

            ingredientes = ingrediente_formset.save(commit=False)
            for ing in ingredientes:
                ing.receta = receta
                ing.save()
            for ing in ingrediente_formset.deleted_objects:
                ing.delete()

            pasos = paso_formset.save(commit=False)
            for i, paso in enumerate(pasos, 1):
                paso.receta = receta
                paso.numero = i
                paso.save()
            for paso in paso_formset.deleted_objects:
                paso.delete()

            return redirect('landing')
    else:
        form = RecetaForm()
        ingrediente_formset = IngredienteFormSet(prefix='ingredientes')
        paso_formset = PasoFormSet(prefix='pasos')

    etiquetas_seleccionadas_ids = [int(x) for x in request.POST.getlist('etiquetas')] if request.method == 'POST' else []

    return render(request, 'landing/recipes.html', {
        'form': form,
        'ingrediente_formset': ingrediente_formset,
        'paso_formset': paso_formset,
        'etiquetas_disponibles': Etiqueta.objects.all(),
        'etiquetas_seleccionadas_ids': etiquetas_seleccionadas_ids,
    })
