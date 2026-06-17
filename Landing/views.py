from django.shortcuts import render


# Create your views here.
def landing(request):
    return render(request, "landing/landing.html")


def about(request):
    return render(request, "landing/about.html")


def challenges(request):
    return render(request, "landing/challenges.html")


def collection(request):
    return render(request, "landing/collection.html")


def recipes(request):
    return render(request, "landing/recipes.html")
