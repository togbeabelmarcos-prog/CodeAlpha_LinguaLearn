from django.conf import settings
from django.db import models


class Profile(models.Model):
    """Profil étendu lié à l'utilisateur Django natif (auth.User)."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    current_language = models.CharField(max_length=5, default="en")
    dark_mode = models.BooleanField(default=False)
    notifications_enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profil de {self.user.username}"
