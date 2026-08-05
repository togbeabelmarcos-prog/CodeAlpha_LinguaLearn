import random
from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from learning.models import Favorite, QuizResult

from .models import Answer, Category, Lesson, Quiz, Vocabulary


def _active_language(request):
    return request.user.profile.current_language if request.user.is_authenticated else "en"


@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, "content/category_list.html", {"categories": categories})


@login_required
def vocabulary_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    language = _active_language(request)
    words = Vocabulary.objects.filter(category=category, language__code=language)
    favorite_ids = set(
        Favorite.objects.filter(user=request.user, vocabulary__in=words).values_list(
            "vocabulary_id", flat=True
        )
    )
    return render(
        request,
        "content/vocabulary_list.html",
        {"category": category, "words": words, "favorite_ids": favorite_ids},
    )


@login_required
@require_POST
def toggle_favorite(request, vocab_id):
    vocabulary = get_object_or_404(Vocabulary, id=vocab_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, vocabulary=vocabulary)
    if not created:
        favorite.delete()
    else:
        request.user.progress.register_words_learned(1)
    next_url = request.POST.get("next") or "content:category_list"
    return redirect(next_url)


@login_required
def grammar_list(request):
    language = _active_language(request)
    lessons = Lesson.objects.filter(language__code=language).prefetch_related("examples").order_by(
        "order"
    )

    from learning.models import LessonProgress

    done_ids = set(
        LessonProgress.objects.filter(user=request.user, lesson__in=lessons).values_list(
            "lesson_id", flat=True
        )
    )

    levels = [
        ("debutant", "Débutant", "🌱"),
        ("intermediaire", "Intermédiaire", "🚀"),
        ("avance", "Avancé", "🏔️"),
    ]
    grouped = []
    for level_code, level_label, icon in levels:
        level_lessons = [l for l in lessons if l.level == level_code]
        if level_lessons:
            grouped.append({"code": level_code, "label": level_label, "icon": icon, "lessons": level_lessons})

    return render(
        request,
        "content/grammar_list.html",
        {"grouped": grouped, "done_ids": done_ids},
    )


@login_required
@require_POST
def mark_lesson_done(request, lesson_id):
    from learning.models import LessonProgress

    lesson = get_object_or_404(Lesson, id=lesson_id)
    _, created = LessonProgress.objects.get_or_create(user=request.user, lesson=lesson)
    if created:
        request.user.progress.register_lesson_completed()
        messages.success(request, f"Leçon « {lesson.title} » marquée comme terminée !")
    return redirect("content:grammar_list")


@login_required
def flashcards_view(request):
    language = _active_language(request)
    words = list(Vocabulary.objects.filter(language__code=language))
    favorite_ids = set(
        Favorite.objects.filter(user=request.user, vocabulary__in=words).values_list(
            "vocabulary_id", flat=True
        )
    )
    return render(
        request,
        "content/flashcards.html",
        {"words": words, "favorite_ids": favorite_ids},
    )


def _daily_quiz_for(language_code):
    """Choisit un quiz de façon déterministe pour la journée en cours,
    identique pour tous les utilisateurs d'une même langue ce jour-là."""
    quizzes = list(Quiz.objects.filter(language__code=language_code).order_by("id"))
    if not quizzes:
        return None
    today_ordinal = date.today().toordinal()
    return quizzes[today_ordinal % len(quizzes)]


@login_required
def quiz_list(request):
    language = _active_language(request)
    quizzes = Quiz.objects.filter(language__code=language).select_related("category")

    daily_quiz = _daily_quiz_for(language)
    daily_done = False
    if daily_quiz:
        daily_done = QuizResult.objects.filter(
            user=request.user, quiz=daily_quiz, completed_at__date=timezone.localdate()
        ).exists()

    by_category = {}
    for quiz in quizzes:
        cat_name = quiz.category.name if quiz.category else "Autres"
        cat_icon = quiz.category.icon if quiz.category else "📚"
        by_category.setdefault((cat_name, cat_icon), []).append(quiz)

    sections = [
        {"name": name, "icon": icon, "quizzes": sorted(qs, key=lambda q: q.level)}
        for (name, icon), qs in sorted(by_category.items())
    ]

    return render(
        request,
        "content/quiz_list.html",
        {
            "sections": sections,
            "daily_quiz": daily_quiz,
            "daily_done": daily_done,
        },
    )


@login_required
def quiz_daily_start(request):
    language = _active_language(request)
    quiz = _daily_quiz_for(language)
    if not quiz:
        messages.info(request, "Aucun quiz disponible pour cette langue pour le moment.")
        return redirect("dashboard:home")
    return quiz_start(request, quiz.id, is_daily=True)


@login_required
def quiz_start(request, quiz_id, is_daily=False):
    quiz = get_object_or_404(Quiz.objects.prefetch_related("questions__answers"), id=quiz_id)

    questions = []
    for question in quiz.questions.all():
        answers = list(question.answers.all())
        random.shuffle(answers)
        questions.append(
            {
                "id": question.id,
                "text": question.text,
                "answers": [{"id": a.id, "text": a.text, "is_correct": a.is_correct} for a in answers],
            }
        )

    if not questions:
        messages.info(request, "Ce quiz ne contient pas encore de questions.")
        return redirect("content:quiz_list")

    request.session["quiz_id"] = quiz.id
    request.session["quiz_title"] = quiz.title
    request.session["quiz_level"] = quiz.get_level_display()
    request.session["quiz_questions"] = questions
    request.session["quiz_index"] = 0
    request.session["quiz_score"] = 0
    request.session["quiz_is_daily"] = is_daily

    return redirect("content:quiz_question")


@login_required
def quiz_question(request):
    questions = request.session.get("quiz_questions")
    index = request.session.get("quiz_index", 0)

    if not questions:
        return redirect("content:quiz_list")

    if index >= len(questions):
        return redirect("content:quiz_result")

    question = questions[index]
    return render(
        request,
        "content/quiz_question.html",
        {
            "question": question,
            "index": index,
            "total": len(questions),
            "quiz_title": request.session.get("quiz_title", ""),
            "quiz_level": request.session.get("quiz_level", ""),
        },
    )


@login_required
@require_POST
def quiz_answer(request):
    questions = request.session.get("quiz_questions")
    index = request.session.get("quiz_index", 0)
    if not questions or index >= len(questions):
        return redirect("content:quiz_list")

    question = questions[index]
    answer_id = request.POST.get("answer_id")

    is_correct = False
    if answer_id:
        answer = Answer.objects.filter(id=answer_id, question_id=question["id"]).first()
        is_correct = bool(answer and answer.is_correct)
        if is_correct:
            request.session["quiz_score"] = request.session.get("quiz_score", 0) + 1

    request.session["quiz_index"] = index + 1
    request.session.modified = True

    return redirect("content:quiz_question")


@login_required
def quiz_result(request):
    quiz_id = request.session.get("quiz_id")
    questions = request.session.get("quiz_questions") or []
    score = request.session.get("quiz_score", 0)
    is_daily = request.session.get("quiz_is_daily", False)

    if not quiz_id:
        return redirect("dashboard:home")

    quiz = get_object_or_404(Quiz, id=quiz_id)
    total = len(questions)

    result = QuizResult.objects.create(
        user=request.user,
        quiz=quiz,
        score=score,
        total_questions=total,
    )
    request.user.progress.register_activity()

    for key in ["quiz_id", "quiz_title", "quiz_level", "quiz_questions", "quiz_index", "quiz_score", "quiz_is_daily"]:
        request.session.pop(key, None)

    return render(request, "content/quiz_result.html", {"result": result, "is_daily": is_daily})
