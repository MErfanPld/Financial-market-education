from django.contrib import admin
from .models import Blog, Category, Tag, Author,Comment


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


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "blog", "user", "content_snippet", "parent", "is_approved", "created_at")
    list_filter = ("is_approved", "created_at")
    search_fields = ("content", "user__phone_number", "user__first_name", "user__last_name")

    def content_snippet(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_snippet.short_description = "متن کامنت"