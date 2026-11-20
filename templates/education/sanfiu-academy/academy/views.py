from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .forms import SignUpForm
from .models import Course, Enrollment, Lesson, LessonProgress


def course_list(request):
    courses = Course.objects.filter(is_published=True).annotate(published_lesson_count=Count("lessons", filter=Q(lessons__is_published=True), distinct=True))
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    if query:
        courses = courses.filter(Q(title__icontains=query) | Q(summary__icontains=query) | Q(instructor__icontains=query))
    if category in dict(Course.CATEGORY_CHOICES):
        courses = courses.filter(category=category)
    featured_course = courses.filter(is_featured=True).first()
    return render(request, "academy/course_list.html", {
        "courses": courses, "featured_course": featured_course, "query": query, "selected_category": category,
    })


def course_detail(request, slug):
    course = get_object_or_404(Course.objects.filter(is_published=True), slug=slug)
    enrollment = None
    if request.user.is_authenticated:
        enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
    lessons = course.published_lessons
    return render(request, "academy/course_detail.html", {"course": course, "lessons": lessons, "enrollment": enrollment})


@login_required
def dashboard(request):
    enrollments = Enrollment.objects.filter(user=request.user).select_related("course").prefetch_related("lesson_progress__lesson")
    return render(request, "academy/dashboard.html", {"enrollments": enrollments})


@require_POST
@login_required
def enroll(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)
    if created:
        messages.success(request, "You are enrolled. Your course is ready.")
    else:
        messages.info(request, "You are already enrolled in this course.")
    return redirect("course_detail", slug=course.slug)


def lesson_detail(request, course_slug, lesson_slug):
    course = get_object_or_404(Course, slug=course_slug, is_published=True)
    lesson = get_object_or_404(Lesson, course=course, slug=lesson_slug, is_published=True)
    enrollment = None
    if request.user.is_authenticated:
        enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
    if enrollment is None and not lesson.is_preview:
        messages.info(request, "Enroll in this course to unlock the lesson.")
        return redirect("course_detail", slug=course.slug)
    lessons = list(course.published_lessons)
    index = lessons.index(lesson)
    previous_lesson = lessons[index - 1] if index > 0 else None
    next_lesson = lessons[index + 1] if index + 1 < len(lessons) else None
    progress = LessonProgress.objects.filter(enrollment=enrollment, lesson=lesson).first() if enrollment else None
    return render(request, "academy/lesson_detail.html", {
        "course": course, "enrollment": enrollment, "lesson": lesson,
        "previous_lesson": previous_lesson, "next_lesson": next_lesson, "progress": progress,
    })


@require_POST
@login_required
def complete_lesson(request, course_slug, lesson_slug):
    course = get_object_or_404(Course, slug=course_slug, is_published=True)
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)
    lesson = get_object_or_404(Lesson, course=course, slug=lesson_slug, is_published=True)
    LessonProgress.objects.update_or_create(enrollment=enrollment, lesson=lesson, defaults={"completed": True})
    messages.success(request, "Progress saved.")
    next_lesson = course.published_lessons.filter(position__gt=lesson.position).first()
    if next_lesson:
        return redirect("lesson_detail", course_slug=course.slug, lesson_slug=next_lesson.slug)
    return redirect("dashboard")


def signup(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Your account is ready. Choose a course to get started.")
        next_url = request.POST.get("next") or request.GET.get("next")
        if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
            return redirect(next_url)
        return redirect("course_list")
    return render(request, "registration/signup.html", {"form": form, "next": request.GET.get("next", "")})
