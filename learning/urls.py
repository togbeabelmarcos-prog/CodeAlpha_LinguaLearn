from django.urls import path

from . import views

app_name = "learning"

urlpatterns = [
    path("favoris/", views.favorites_view, name="favorites"),
    path("progression/", views.progress_view, name="progress"),
]
