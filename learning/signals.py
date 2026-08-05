from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Progress


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_progress(sender, instance, created, **kwargs):
    """Crée automatiquement un enregistrement de progression pour chaque nouvel utilisateur."""
    if created:
        Progress.objects.get_or_create(user=instance)
