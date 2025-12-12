from django.contrib import admin
from .models import Blog, Category, Tag, Author


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("full_name", "experience_years")


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "author", "reading_time", "views", "created_at")
    list_filter = ("category", "tags")
    search_fields = ("title", "excerpt", "author__full_name")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags",)
