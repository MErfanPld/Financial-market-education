from django.contrib import admin
from .models import (
    Instructor,
    Course,
    Lesson,
    Review,
    UserProgress,
    LessonProgress,
)


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email")
    search_fields = ("full_name", "email")


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    fields = ("order", "title", "video", "duration_minutes", "is_free")
    ordering = ("order",)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "instructor",
        "duration_weeks",
        "total_sessions",
        "rating",
    )
    list_filter = ("instructor",)
    search_fields = ("title", "description")
    inlines = [LessonInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("course", "user", "rate", "created_at")
    list_filter = ("rate", "created_at")
    search_fields = ("comment",)
    readonly_fields = ("created_at",)


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "course",
        "completed_lessons",
        "progress_percent_display",
    )
    list_filter = ("course",)
    readonly_fields = ("completed_lessons",)

    def progress_percent_display(self, obj):
        return f"{obj.progress_percent}٪"

    progress_percent_display.short_description = "درصد پیشرفت"


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "lesson", "is_completed")
    list_filter = ("is_completed", "lesson__course")
    search_fields = ("user__username", "lesson__title")
