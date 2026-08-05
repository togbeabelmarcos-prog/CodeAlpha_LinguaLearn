from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from content.models import Category, Lesson


@login_required
def home(request):
    language = request.user.profile.current_language
    today_lesson = Lesson.objects.filter(language__code=language).order_by("order").first()
    categories = Category.objects.all()[:4]
    progress = request.user.progress
    return render(
        request,
        "dashboard/home.html",
        {
            "today_lesson": today_lesson,
            "categories": categories,
            "progress": progress,
        },
    )
