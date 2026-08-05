from django.contrib import admin
from .models import Language, Category, Vocabulary, Lesson, LessonExample, Quiz, Question, Answer


class LessonExampleInline(admin.TabularInline):
    model = LessonExample
    extra = 1


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 2


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "flag_emoji")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "icon")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Vocabulary)
class VocabularyAdmin(admin.ModelAdmin):
    list_display = ("word", "translation", "language", "category")
    list_filter = ("language", "category")
    search_fields = ("word", "translation")


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "language", "level", "order")
    list_filter = ("language", "level")
    inlines = [LessonExampleInline]


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("title", "language", "category")
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "quiz")
    inlines = [AnswerInline]
