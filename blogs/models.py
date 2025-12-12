from django.db import models
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField


class Category(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان دسته")
    slug = models.SlugField(unique=True, blank=True, verbose_name="آدرس دسته")
    description = models.TextField(null=True, blank=True, verbose_name="توضیحات")

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"
        ordering = ("title",)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=100, verbose_name="عنوان تگ")
    slug = models.SlugField(unique=True, blank=True, verbose_name="آدرس تگ")

    class Meta:
        verbose_name = "تگ"
        verbose_name_plural = "تگ‌ها"
        ordering = ("title",)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Author(models.Model):
    full_name = models.CharField(max_length=150, verbose_name="نام نویسنده")
    description = models.TextField(verbose_name="بیوگرافی")
    avatar = models.ImageField(
        upload_to="uploads/authors/",
        null=True,
        blank=True,
        verbose_name="تصویر پروفایل"
    )
    experience_years = models.PositiveIntegerField(default=1, verbose_name="سال‌های سابقه")

    class Meta:
        verbose_name = "نویسنده"
        verbose_name_plural = "نویسندگان"
        ordering = ("full_name",)

    def __str__(self):
        return self.full_name


class Blog(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="blogs",
        verbose_name="دسته‌بندی"
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="نویسنده"
    )
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="تگ‌ها")

    title = models.CharField(max_length=300, verbose_name="عنوان مقاله")
    slug = models.SlugField(unique=True, blank=True, max_length=350, verbose_name="آدرس مقاله")

    excerpt = models.CharField(max_length=400, verbose_name="خلاصه کوتاه")
    content = RichTextUploadingField(verbose_name="محتوا")

    reading_time = models.PositiveIntegerField(default=5, verbose_name="زمان مطالعه (دقیقه)")
    cover = models.ImageField(
        upload_to="uploads/articles/",
        null=True,
        blank=True,
        verbose_name="تصویر کاور"
    )

    views = models.PositiveIntegerField(default=0, verbose_name="تعداد بازدید")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)

        # محاسبه حرفه‌ای زمان مطالعه (150 کلمه = 1 دقیقه)
        clean_text = (
            self.content.replace("<", " ")
            .replace(">", " ")
            .replace("&nbsp;", " ")
            .replace("\n", " ")
        )
        word_count = len(clean_text.split())
        self.reading_time = max(1, int(word_count / 150))

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
