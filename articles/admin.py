from django.contrib import admin
from .models import Category, Article, ArticleSection, ArticleImage


class ArticleSectionInline(admin.StackedInline):
    model = ArticleSection
    extra = 1


class ArticleImageInline(admin.TabularInline):
    model = ArticleImage
    extra = 1


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "jcreated")
    list_filter = ("category", "author")
    search_fields = ("title", "summary")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ArticleSectionInline, ArticleImageInline]


admin.site.register(Category)
