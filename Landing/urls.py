from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing, name="landing"),
    path("about/", views.about, name="about"),
    path("challenges/", views.challenges, name="challenges"),
    path("collection/", views.collection, name="collection"),
    path("recipes/", views.recipes, name="recipes"),
]
