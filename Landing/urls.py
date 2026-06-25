from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing, name="landing"),
    path("about/", views.about, name="about"),
    path("challenges/", views.challenges, name="challenges"),
    path("explorar/", views.explorar, name="explorar"),
    path("explorar/<int:pk>/", views.receta_detalle, name="receta_detalle"),
    path("explorar/<int:pk>/editar/", views.receta_editar, name="receta_editar"),
    path("explorar/<int:pk>/eliminar/", views.receta_eliminar, name="receta_eliminar"),
    path("recipes/", views.recipes, name="recipes"),
    path("etiquetas/crear/", views.etiqueta_crear, name="etiqueta_crear"),
    path("etiquetas/<int:pk>/editar/", views.etiqueta_editar, name="etiqueta_editar"),
    path("etiquetas/<int:pk>/eliminar/", views.etiqueta_eliminar, name="etiqueta_eliminar"),
]
