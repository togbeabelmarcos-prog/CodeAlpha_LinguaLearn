from django.db import models


class Language(models.Model):
    code = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=50)
    flag_emoji = models.CharField(max_length=8, default="")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Category(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=8, default="📘")

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Vocabulary(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name="vocabulary")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="vocabulary")
    word = models.CharField(max_length=120)
    translation = models.CharField(max_length=120)
    pronunciation = models.CharField(max_length=120, blank=True)
    example = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to="vocabulary/", blank=True, null=True)
    audio = models.FileField(upload_to="vocabulary_audio/", blank=True, null=True)

    class Meta:
        verbose_name_plural = "Vocabulary"
        ordering = ["word"]

    def __str__(self):
        return f"{self.word} ({self.language.code})"


class Lesson(models.Model):
    LEVEL_CHOICES = [
        ("debutant", "Débutant"),
        ("intermediaire", "Intermédiaire"),
        ("avance", "Avancé"),
    ]

    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=150)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default="debutant")
    explanation = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class LessonExample(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="examples")
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


class Quiz(models.Model):
    LEVEL_CHOICES = [
        ("debutant", "Débutant"),
        ("intermediaire", "Intermédiaire"),
        ("avance", "Avancé"),
    ]

    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name="quizzes")
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name="quizzes", null=True, blank=True
    )
    title = models.CharField(max_length=150)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default="debutant")

    class Meta:
        ordering = ["category__name", "level"]

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    text = models.CharField(max_length=150)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
