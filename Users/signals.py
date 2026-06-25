from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()


@receiver(post_save, sender=User)
def asignar_grupo_cocinero(sender, instance, created, **kwargs):
   
    if created and not instance.is_superuser:
        try:
            grupo = Group.objects.get(name='Cocinero')
            instance.groups.add(grupo)
        except Group.DoesNotExist:
            pass
