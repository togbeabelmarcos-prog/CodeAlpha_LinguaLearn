from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from content.models import Language
from .models import Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")
    first_name = forms.CharField(required=True, label="Nom complet")

    class Meta:
        model = User
        fields = ["first_name", "email", "username", "password1", "password2"]
        labels = {"username": "Nom d'utilisateur"}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class ProfileSettingsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["current_language", "dark_mode", "notifications_enabled"]
        widgets = {
            "current_language": forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["current_language"].widget.choices = [
            (l.code, f"{l.flag_emoji} {l.name}") for l in Language.objects.all()
        ]
