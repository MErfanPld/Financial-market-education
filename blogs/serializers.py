from rest_framework import serializers
from .models import Blog, Category, Tag, Author,Comment


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "full_name", "avatar", "description", "experience_years"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title", "slug"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "title", "slug"]


class BlogListSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    category = CategorySerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = Blog
        fields = [
            "id", "title", "slug", "excerpt", "cover",
            "author", "category", "tags",'telegram','instagram','youtube','x' ,"reading_time", "created_at"
            ]


class BlogDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    category = CategorySerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = Blog
        fields = "__all__"



class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ["id", "blog", "user", "user_name", "parent", "content", "is_approved", "created_at", "replies"]
        read_only_fields = ["is_approved", "created_at", "replies", "user_name"]

    def get_replies(self, obj):
        qs = obj.children
        return CommentSerializer(qs, many=True).data

    def get_user_name(self, obj):
        if obj.user:
            return obj.user.get_full_name()
        return "کاربر مهمان"