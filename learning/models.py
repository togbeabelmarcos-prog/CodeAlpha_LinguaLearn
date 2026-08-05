from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone

from content.models import Vocabulary, Lesson, Quiz


class Badge(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    icon = models.CharField(max_length=8, default="🏅")
    required_value = models.PositiveIntegerField(default=1)
    METRIC_CHOICES = [
        ("lessons", "Leçons terminées"),
        ("words", "Mots appris"),
        ("streak", "Série quotidienne"),
    ]
    metric = models.CharField(max_length=20, choices=METRIC_CHOICES, default="lessons")

    def __str__(self):
        return self.title


class Progress(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="progress"
    )
    lessons_completed = models.PositiveIntegerField(default=0)
    words_learned = models.PositiveIntegerField(default=0)
    daily_streak = models.PositiveIntegerField(default=0)
    last_activity = models.DateField(default=timezone.localdate)
    badges = models.ManyToManyField(Badge, blank=True, related_name="earned_by")

    def __str__(self):
        return f"Progression de {self.user.username}"

    def register_activity(self):
        """Met à jour la série de jours consécutifs (streak)."""
        today = timezone.localdate()
        if self.last_activity == today:
            if self.daily_streak == 0:
                self.daily_streak = 1  # toute première activité de l'utilisateur
        elif self.last_activity == today - timedelta(days=1):
            self.daily_streak += 1
        else:
            self.daily_streak = 1
        self.last_activity = today
        self.save()
        self.refresh_badges()

    def register_lesson_completed(self):
        self.lessons_completed += 1
        self.register_activity()

    def register_words_learned(self, count=1):
        self.words_learned += count
        self.register_activity()

    def refresh_badges(self):
        for badge in Badge.objects.all():
            value = {
                "lessons": self.lessons_completed,
                "words": self.words_learned,
                "streak": self.daily_streak,
            }.get(badge.metric, 0)
            if value >= badge.required_value:
                self.badges.add(badge)


class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favorites"
    )
    vocabulary = models.ForeignKey(Vocabulary, on_delete=models.CASCADE, related_name="favorited_by")
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "vocabulary")

    def __str__(self):
        return f"{self.user.username} ♥ {self.vocabulary.word}"


class QuizResult(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="quiz_results"
    )
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="results")
    score = models.PositiveIntegerField()
    total_questions = models.PositiveIntegerField()
    time_spent_seconds = models.PositiveIntegerField(default=0)
    completed_at = models.DateTimeField(auto_now_add=True)

    @property
    def percentage(self):
        if self.total_questions == 0:
            return 0
        return round((self.score / self.total_questions) * 100)

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} : {self.score}/{self.total_questions}"


class LessonProgress(models.Model):
    """Suivi des leçons terminées individuellement (pour éviter les doublons)."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="lesson_progress"
    )
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="completions")
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "lesson")
