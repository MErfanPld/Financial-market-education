from rest_framework import serializers
from .models import Category, Article, ArticleSection, ArticleImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title", "slug"]


class ArticleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleImage
        fields = ["id", "image", "alt"]


class ArticleSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleSection
        fields = ["id", "title", "body", "order"]


class ArticleSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.get_full_name", read_only=True)
    sections = ArticleSectionSerializer(many=True, read_only=True)
    images = ArticleImageSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Article
        fields = [
            "id",
            "title",
            "summary",
            "slug",
            "author",
            "author_name",
            "category",
            "sections",
            "images",
            "jcreated",
            "jupdated",
        ]
