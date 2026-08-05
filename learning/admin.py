from django.contrib import admin
from .models import Badge, Progress, Favorite, QuizResult, LessonProgress

admin.site.register(Badge)
admin.site.register(Progress)
admin.site.register(Favorite)
admin.site.register(QuizResult)
admin.site.register(LessonProgress)
