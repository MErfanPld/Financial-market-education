from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Article, Category
from .serializers import ArticleSerializer, CategorySerializer


class ArticleListView(generics.ListAPIView):
    queryset = Article.objects.all().prefetch_related("sections", "images", "category")
    serializer_class = ArticleSerializer
    permission_classes = [AllowAny]


class ArticleDetailView(generics.RetrieveAPIView):
    queryset = Article.objects.all().prefetch_related("sections", "images", "category")
    serializer_class = ArticleSerializer
    lookup_field = "slug"
    permission_classes = [AllowAny]


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
