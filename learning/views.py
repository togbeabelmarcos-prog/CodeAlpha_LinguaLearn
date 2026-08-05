from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Badge, Favorite


@login_required
def favorites_view(request):
    favorites = Favorite.objects.filter(user=request.user).select_related("vocabulary")
    return render(request, "learning/favorites.html", {"favorites": favorites})


@login_required
def progress_view(request):
    progress, _ = request.user.progress, None
    all_badges = Badge.objects.all()
    earned_ids = set(progress.badges.values_list("id", flat=True))
    return render(
        request,
        "learning/progress.html",
        {
            "progress": progress,
            "all_badges": all_badges,
            "earned_ids": earned_ids,
        },
    )
