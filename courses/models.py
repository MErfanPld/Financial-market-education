from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Instructor(models.Model):
    full_name = models.CharField(
        max_length=150,
        verbose_name="نام و نام خانوادگی"
    )
    email = models.EmailField(
        unique=True,
        verbose_name="ایمیل"
    )

    class Meta:
        verbose_name = "استاد"
        verbose_name_plural = "اساتید"

    def __str__(self):
        return self.full_name


class Course(models.Model):
    instructor = models.ForeignKey(
        Instructor,
        on_delete=models.CASCADE,
        related_name="courses",
        verbose_name="استاد دوره"
    )
    title = models.CharField(
        max_length=200,
        verbose_name="عنوان دوره"
    )
    description = models.TextField(
        verbose_name="درباره دوره"
    )
    duration_weeks = models.PositiveIntegerField(
        verbose_name="مدت دوره (هفته)"
    )
    total_sessions = models.PositiveIntegerField(
        verbose_name="تعداد جلسات"
    )
    rating = models.FloatField(
        default=0,
        verbose_name="امتیاز دوره"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )

    class Meta:
        verbose_name = "دوره آموزشی"
        verbose_name_plural = "دوره‌های آموزشی"

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="دوره"
    )
    title = models.CharField(
        max_length=200,
        verbose_name="عنوان جلسه"
    )
    order = models.PositiveIntegerField(
        verbose_name="ترتیب جلسه"
    )
    video = models.FileField(
        upload_to="courses/lessons/videos/",
        null=True,
        blank=True,
        verbose_name="ویدیو آموزشی"
    )
    duration_minutes = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="مدت ویدیو (دقیقه)"
    )
    is_free = models.BooleanField(
        default=False,
        verbose_name="رایگان"
    )

    class Meta:
        verbose_name = "جلسه"
        verbose_name_plural = "جلسات"
        ordering = ["order"]

    def __str__(self):
        return self.title



class Review(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="دوره"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="کاربر"
    )
    rate = models.PositiveSmallIntegerField(
        verbose_name="امتیاز"
    )
    comment = models.TextField(
        blank=True,
        verbose_name="نظر کاربر"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ثبت"
    )

    class Meta:
        verbose_name = "نظر"
        verbose_name_plural = "نظرات کاربران"

    def __str__(self):
        return f"{self.user} - {self.course}"


class LessonProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name="جلسه")
    is_completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user", "lesson")
        verbose_name = "پیشرفت جلسه"
        verbose_name_plural = "پیشرفت جلسات"


class UserProgress(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="کاربر"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="دوره"
    )
    completed_lessons = models.PositiveIntegerField(
        default=0,
        verbose_name="تعداد جلسات گذرانده‌شده"
    )

    class Meta:
        verbose_name = "پیشرفت کاربر"
        verbose_name_plural = "پیشرفت کاربران"
        unique_together = ("user", "course")

    @property
    def progress_percent(self):
        return int((self.completed_lessons / self.course.total_sessions) * 100)

    def __str__(self):
        return f"{self.user} - {self.course}"
