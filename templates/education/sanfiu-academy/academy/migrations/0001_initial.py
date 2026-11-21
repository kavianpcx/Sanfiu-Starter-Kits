from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(name="Course", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("title", models.CharField(max_length=150)), ("slug", models.SlugField(max_length=170, unique=True)),
            ("category", models.CharField(choices=[("design", "Design"), ("technology", "Technology"), ("business", "Business"), ("wellbeing", "Wellbeing"), ("creative", "Creative skills")], max_length=24)),
            ("level", models.CharField(choices=[("beginner", "Beginner"), ("intermediate", "Intermediate"), ("advanced", "Advanced")], default="beginner", max_length=16)),
            ("summary", models.CharField(max_length=220)), ("description", models.TextField()),
            ("instructor", models.CharField(max_length=120)), ("estimated_hours", models.DecimalField(decimal_places=1, default=1, max_digits=4)),
            ("cover_image_url", models.URLField(blank=True, max_length=500)), ("is_featured", models.BooleanField(default=False)),
            ("is_published", models.BooleanField(default=False)), ("created_at", models.DateTimeField(auto_now_add=True)),
        ], options={"ordering": ["-is_featured", "title"]}),
        migrations.CreateModel(name="Lesson", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("title", models.CharField(max_length=150)), ("slug", models.SlugField(max_length=170)), ("summary", models.CharField(blank=True, max_length=220)),
            ("content", models.TextField(help_text="Lesson notes. Keep it useful even when a video is added.")),
            ("video_url", models.URLField(blank=True, help_text="Optional link to your hosted lesson video.", max_length=500)),
            ("duration_minutes", models.PositiveSmallIntegerField(default=10)), ("position", models.PositiveSmallIntegerField(default=1)),
            ("is_preview", models.BooleanField(default=False)), ("is_published", models.BooleanField(default=True)),
            ("course", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="lessons", to="academy.course")),
        ], options={"ordering": ["position", "id"]}),
        migrations.CreateModel(name="Enrollment", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("enrolled_at", models.DateTimeField(auto_now_add=True)),
            ("course", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="enrollments", to="academy.course")),
            ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="course_enrollments", to=settings.AUTH_USER_MODEL)),
        ], options={"ordering": ["-enrolled_at"]}),
        migrations.CreateModel(name="LessonProgress", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("completed", models.BooleanField(default=True)), ("completed_at", models.DateTimeField(auto_now=True)),
            ("enrollment", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="lesson_progress", to="academy.enrollment")),
            ("lesson", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="progress_records", to="academy.lesson")),
        ], options={"ordering": ["completed_at"]}),
        migrations.AddConstraint(model_name="lesson", constraint=models.UniqueConstraint(fields=("course", "slug"), name="unique_lesson_slug_per_course")),
        migrations.AddConstraint(model_name="enrollment", constraint=models.UniqueConstraint(fields=("user", "course"), name="unique_course_enrollment")),
        migrations.AddConstraint(model_name="lessonprogress", constraint=models.UniqueConstraint(fields=("enrollment", "lesson"), name="unique_enrollment_lesson_progress")),
    ]
