from django.urls import path

from . import views

app_name = "content"

urlpatterns = [
    path("vocabulaire/", views.category_list, name="category_list"),
    path("vocabulaire/<slug:slug>/", views.vocabulary_list, name="vocabulary_list"),
    path("vocabulaire/favori/<int:vocab_id>/", views.toggle_favorite, name="toggle_favorite"),
    path("grammaire/", views.grammar_list, name="grammar_list"),
    path("grammaire/terminer/<int:lesson_id>/", views.mark_lesson_done, name="mark_lesson_done"),
    path("flashcards/", views.flashcards_view, name="flashcards"),
    path("quiz/", views.quiz_list, name="quiz_list"),
    path("quiz/du-jour/", views.quiz_daily_start, name="quiz_daily_start"),
    path("quiz/<int:quiz_id>/commencer/", views.quiz_start, name="quiz_start"),
    path("quiz/question/", views.quiz_question, name="quiz_question"),
    path("quiz/repondre/", views.quiz_answer, name="quiz_answer"),
    path("quiz/resultat/", views.quiz_result, name="quiz_result"),
]
