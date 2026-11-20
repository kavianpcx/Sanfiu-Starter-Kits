from django.conf import settings
from django.db import models
from django.urls import reverse


class Course(models.Model):
    CATEGORY_CHOICES = [
        ("design", "Design"), ("technology", "Technology"), ("business", "Business"),
        ("wellbeing", "Wellbeing"), ("creative", "Creative skills"),
    ]
    LEVEL_CHOICES = [("beginner", "Beginner"), ("intermediate", "Intermediate"), ("advanced", "Advanced")]

    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True)
    category = models.CharField(max_length=24, choices=CATEGORY_CHOICES)
    level = models.CharField(max_length=16, choices=LEVEL_CHOICES, default="beginner")
    summary = models.CharField(max_length=220)
    description = models.TextField()
    instructor = models.CharField(max_length=120)
    estimated_hours = models.DecimalField(max_digits=4, decimal_places=1, default=1)
    cover_image_url = models.URLField(max_length=500, blank=True)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-is_featured", "title"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("course_detail", kwargs={"slug": self.slug})

    @property
    def published_lessons(self):
        return self.lessons.filter(is_published=True)

    @property
    def lesson_count(self):
        return self.published_lessons.count()


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170)
    summary = models.CharField(max_length=220, blank=True)
    content = models.TextField(help_text="Lesson notes. Keep it useful even when a video is added.")
    video_url = models.URLField(max_length=500, blank=True, help_text="Optional link to your hosted lesson video.")
    duration_minutes = models.PositiveSmallIntegerField(default=10)
    position = models.PositiveSmallIntegerField(default=1)
    is_preview = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["position", "id"]
        constraints = [models.UniqueConstraint(fields=["course", "slug"], name="unique_lesson_slug_per_course")]

    def __str__(self):
        return f"{self.course.title} · {self.title}"


class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="course_enrollments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-enrolled_at"]
        constraints = [models.UniqueConstraint(fields=["user", "course"], name="unique_course_enrollment")]

    def __str__(self):
        return f"{self.user} · {self.course}"

    @property
    def completed_count(self):
        return self.lesson_progress.filter(completed=True, lesson__is_published=True).count()

    @property
    def total_lessons(self):
        return self.course.published_lessons.count()

    @property
    def progress_percent(self):
        total = self.total_lessons
        return round(self.completed_count * 100 / total) if total else 0

    @property
    def next_lesson(self):
        done_ids = self.lesson_progress.filter(completed=True).values_list("lesson_id", flat=True)
        return self.course.published_lessons.exclude(id__in=done_ids).first() or self.course.published_lessons.first()


class LessonProgress(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name="lesson_progress")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="progress_records")
    completed = models.BooleanField(default=True)
    completed_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["completed_at"]
        constraints = [models.UniqueConstraint(fields=["enrollment", "lesson"], name="unique_enrollment_lesson_progress")]

    def __str__(self):
        return f"{self.enrollment.user} · {self.lesson.title}"
