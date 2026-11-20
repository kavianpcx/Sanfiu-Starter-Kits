from django.contrib import admin
from .models import Course, Enrollment, Lesson, LessonProgress

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0
    fields = ("position", "title", "slug", "duration_minutes", "is_preview", "is_published")
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "level", "instructor", "is_featured", "is_published")
    list_filter = ("category", "level", "is_published", "is_featured")
    list_editable = ("is_featured", "is_published")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "summary", "instructor")
    inlines = [LessonInline]

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "enrolled_at")
    list_filter = ("course", "enrolled_at")
    search_fields = ("user__username", "user__email", "course__title")
    readonly_fields = ("user", "course", "enrolled_at")
    fields = readonly_fields

@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ("enrollment", "lesson", "completed", "completed_at")
    list_filter = ("completed", "lesson__course")
    search_fields = ("enrollment__user__username", "lesson__title", "lesson__course__title")
    readonly_fields = ("enrollment", "lesson", "completed", "completed_at")
    fields = readonly_fields
