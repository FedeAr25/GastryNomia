from django.db import models
from django.conf import settings

_COLORES = {
    "orange": {"bg": "#fff7ed", "text": "#ea580c", "border": "#f97316"},
    "blue": {"bg": "#eff6ff", "text": "#2563eb", "border": "#3b82f6"},
    "green": {"bg": "#f0fdf4", "text": "#16a34a", "border": "#22c55e"},
    "yellow": {"bg": "#fefce8", "text": "#ca8a04", "border": "#eab308"},
    "pink": {"bg": "#fdf2f8", "text": "#db2777", "border": "#ec4899"},
    "amber": {"bg": "#fffbeb", "text": "#d97706", "border": "#f59e0b"},
    "purple": {"bg": "#faf5ff", "text": "#9333ea", "border": "#a855f7"},
    "red": {"bg": "#fef2f2", "text": "#dc2626", "border": "#ef4444"},
}


class Etiqueta(models.Model):
    COLOR_CHOICES = [
        ("orange", "Naranja"),
        ("blue", "Azul"),
        ("green", "Verde"),
        ("yellow", "Amarillo"),
        ("pink", "Rosa"),
        ("amber", "Ámbar"),
        ("purple", "Morado"),
        ("red", "Rojo"),
    ]

    nombre = models.CharField(max_length=50)
    color = models.CharField(max_length=10, choices=COLOR_CHOICES, default="orange")

    def __str__(self):
        return self.nombre

    def get_badge_style(self):
        c = _COLORES.get(self.color, _COLORES["orange"])
        return f"background-color:{c['bg']};color:{c['text']};"

    def get_badge_style_selected(self):
        c = _COLORES.get(self.color, _COLORES["orange"])
        return f"background-color:{c['bg']};color:{c['text']};outline:2px solid {c['border']};font-weight:600;"


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Receta(models.Model):
    DIFICULTAD_CHOICES = [
        ("facil", "Fácil"),
        ("media", "Media"),
        ("dificil", "Difícil"),
        ("extrema", "Extrema"),
    ]

    nombre = models.CharField(max_length=200)
    imagen = models.ImageField(upload_to="recetas/", null=True, blank=True)
    tiempo = models.CharField(max_length=50)
    porciones = models.PositiveIntegerField()
    dificultad = models.CharField(max_length=10, choices=DIFICULTAD_CHOICES)
    categorias = models.ManyToManyField(Categoria, blank=True)
    etiquetas = models.ManyToManyField(Etiqueta, blank=True)
    notas = models.TextField(blank=True)
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="recetas"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = [
            ("can_manage_all_recetas", "Puede gestionar cualquier receta"),
        ]

    def __str__(self):
        return self.nombre


class Ingrediente(models.Model):
    receta = models.ForeignKey(
        Receta, on_delete=models.CASCADE, related_name="ingredientes"
    )
    descripcion = models.CharField(max_length=300)

    def __str__(self):
        return self.descripcion


class PasoInstruccion(models.Model):
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name="pasos")
    numero = models.PositiveIntegerField()
    descripcion = models.TextField()

    class Meta:
        ordering = ["numero"]

    def __str__(self):
        return f"Paso {self.numero}"
