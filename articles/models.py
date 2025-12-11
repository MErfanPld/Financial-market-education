from django.db import models
from django.conf import settings
from django.utils.text import slugify
from ckeditor.fields import RichTextField

from extenstions.utils import jalali_converter


class Category(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="عنوان دسته‌بندی"
    )
    slug = models.SlugField(
        unique=True,
        blank=True,
        verbose_name="اسلاگ"
    )

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"
        ordering = ["title"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Article(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="articles",
        verbose_name="نویسنده"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="articles",
        verbose_name="دسته‌بندی"
    )
    title = models.CharField(
        max_length=255,
        verbose_name="عنوان مقاله"
    )
    summary = models.TextField(
        blank=True,
        verbose_name="خلاصه"
    )
    slug = models.SlugField(
        unique=True,
        blank=True,
        verbose_name="اسلاگ"
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name="آخرین بروزرسانی"
    )

    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"
        ordering = ["-created"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


    def jcreated(self):
        return jalali_converter(self.created)
    jcreated.short_description = "تاریخ ساخت"


    def jupdated(self):
        return jalali_converter(self.updated)
    jupdated.short_description = "تاریخ بروز رسانی"
    

class ArticleSection(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="sections",
        verbose_name="مقاله"
    )
    title = models.CharField(
        max_length=255,
        verbose_name="عنوان سرفصل"
    )
    body = RichTextField(
        verbose_name="متن سرفصل"
    )
    order = models.PositiveIntegerField(
        default=1,
        verbose_name="ترتیب نمایش"
    )

    class Meta:
        verbose_name = "سرفصل مقاله"
        verbose_name_plural = "سرفصل‌های مقاله"
        ordering = ["order"]

    def __str__(self):
        return f"{self.article.title} - {self.title}"


class ArticleImage(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="مقاله"
    )
    image = models.ImageField(
        upload_to="articles/images/",
        verbose_name="تصویر"
    )
    alt = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="متن ALT تصویر"
    )

    class Meta:
        verbose_name = "تصویر مقاله"
        verbose_name_plural = "تصاویر مقاله"

    def __str__(self):
        return f"Image for {self.article.title}"
