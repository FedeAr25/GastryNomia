from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import RecetaForm, IngredienteFormSet, PasoFormSet, EtiquetaForm
from .models import Etiqueta, Receta
import json


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


def receta_detalle(request, pk):
    receta = get_object_or_404(
        Receta.objects.select_related('autor').prefetch_related('ingredientes', 'pasos', 'etiquetas', 'categorias'),
        pk=pk
    )
    return render(request, 'landing/receta_detalle.html', {'receta': receta})


@login_required
def receta_editar(request, pk):
    receta = get_object_or_404(Receta, pk=pk)
    es_autor = receta.autor == request.user
    es_editor = request.user.has_perm('Landing.can_manage_all_recetas')
    if not (es_autor or es_editor):
        return redirect('explorar')

    if request.method == 'POST':
        form = RecetaForm(request.POST, request.FILES, instance=receta)
        ingrediente_formset = IngredienteFormSet(request.POST, instance=receta, prefix='ingredientes')
        paso_formset = PasoFormSet(request.POST, instance=receta, prefix='pasos')

        if form.is_valid() and ingrediente_formset.is_valid() and paso_formset.is_valid():
            form.save()

            ingredientes = ingrediente_formset.save(commit=False)
            for ing in ingredientes:
                ing.receta = receta
                ing.save()
            for ing in ingrediente_formset.deleted_objects:
                ing.delete()

            pasos = paso_formset.save(commit=False)
            for paso in pasos:
                paso.receta = receta
                paso.save()
            for paso in paso_formset.deleted_objects:
                paso.delete()
            for i, paso in enumerate(receta.pasos.all(), 1):
                paso.numero = i
                paso.save(update_fields=['numero'])

            return redirect('receta_detalle', pk=receta.pk)
    else:
        form = RecetaForm(instance=receta)
        ingrediente_formset = IngredienteFormSet(instance=receta, prefix='ingredientes')
        paso_formset = PasoFormSet(instance=receta, prefix='pasos')

    etiquetas_seleccionadas_ids = list(receta.etiquetas.values_list('pk', flat=True))

    return render(request, 'landing/receta_editar.html', {
        'form': form,
        'ingrediente_formset': ingrediente_formset,
        'paso_formset': paso_formset,
        'etiquetas_disponibles': Etiqueta.objects.all(),
        'etiquetas_seleccionadas_ids': etiquetas_seleccionadas_ids,
        'receta': receta,
    })


@login_required
def receta_eliminar(request, pk):
    receta = get_object_or_404(Receta, pk=pk)
    es_autor = receta.autor == request.user
    es_editor = request.user.has_perm('Landing.can_manage_all_recetas')
    if not (es_autor or es_editor):
        return redirect('explorar')

    if request.method == 'POST':
        receta.delete()
        return redirect('explorar')

    return render(request, 'landing/receta_eliminar.html', {'receta': receta})


def _ajax_forbidden(request):
    """Responde 403 en AJAX o redirige al explorar en peticiones normales."""
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'ok': False, 'error': 'Sin permisos'}, status=403)
    return redirect('explorar')


@login_required
def etiqueta_crear(request):
    if not request.user.has_perm('Landing.add_etiqueta'):
        return _ajax_forbidden(request)
    if request.method == 'POST':
        form = EtiquetaForm(request.POST)
        if form.is_valid():
            etiqueta = form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'ok': True,
                    'pk': etiqueta.pk,
                    'nombre': etiqueta.nombre,
                    'color': etiqueta.color,
                    'badge_style': etiqueta.get_badge_style(),
                    'badge_style_sel': etiqueta.get_badge_style_selected(),
                })
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'ok': False})
    return redirect('recipes')


@login_required
def etiqueta_editar(request, pk):
    if not request.user.has_perm('Landing.change_etiqueta'):
        return _ajax_forbidden(request)
    etiqueta = get_object_or_404(Etiqueta, pk=pk)
    if request.method == 'POST':
        form = EtiquetaForm(request.POST, instance=etiqueta)
        if form.is_valid():
            etiqueta = form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'ok': True,
                    'pk': etiqueta.pk,
                    'nombre': etiqueta.nombre,
                    'color': etiqueta.color,
                    'badge_style': etiqueta.get_badge_style(),
                    'badge_style_sel': etiqueta.get_badge_style_selected(),
                })
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'ok': False})
    return redirect('recipes')


@login_required
def etiqueta_eliminar(request, pk):
    if not request.user.has_perm('Landing.delete_etiqueta'):
        return _ajax_forbidden(request)
    if request.method == 'POST':
        etiqueta = get_object_or_404(Etiqueta, pk=pk)
        etiqueta.delete()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'ok': True})
    return redirect('recipes')


@login_required
def recipes(request):
    if not request.user.has_perm('Landing.add_receta'):
        return redirect('explorar')

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

            return redirect('explorar')
    else:
        form = RecetaForm()
        ingrediente_formset = IngredienteFormSet(prefix='ingredientes')
        paso_formset = PasoFormSet(prefix='pasos')

    etiquetas_seleccionadas_ids = [int(x) for x in request.POST.getlist('etiquetas')] if request.method == 'POST' else []
    color_choices_json = json.dumps([[val, label] for val, label in Etiqueta.COLOR_CHOICES])

    return render(request, 'landing/recipes.html', {
        'form': form,
        'ingrediente_formset': ingrediente_formset,
        'paso_formset': paso_formset,
        'etiquetas_disponibles': Etiqueta.objects.all(),
        'etiquetas_seleccionadas_ids': etiquetas_seleccionadas_ids,
        'color_choices': Etiqueta.COLOR_CHOICES,
        'color_choices_json': color_choices_json,
    })
