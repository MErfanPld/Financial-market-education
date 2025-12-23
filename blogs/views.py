from rest_framework import generics
from rest_framework.permissions import AllowAny,IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from blogs.filters import BlogFilter
from .models import *
from .serializers import *


class BlogListView(generics.ListAPIView):
    queryset = Blog.objects.select_related("author", "category").prefetch_related("tags")
    serializer_class = BlogListSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BlogFilter
    search_fields = ['title', 'excerpt', 'content']
    ordering_fields = ['created_at', 'views']

class BlogDetailView(generics.RetrieveAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogDetailSerializer
    lookup_field = "slug"
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        blog = self.get_object()
        blog.views += 1
        blog.save(update_fields=["views"])
        return super().get(request, *args, **kwargs)



class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        blog_id = self.kwargs.get("blog_id")
        slug = self.kwargs.get("slug")
        return Comment.objects.filter(
            blog_id=blog_id, 
            blog__slug=slug, 
            parent=None, 
            is_approved=True
        ).select_related("user")

    def perform_create(self, serializer):
        blog_id = self.kwargs.get("blog_id")
        serializer.save(user=self.request.user, blog_id=blog_id)



class CategoryBlogListAPIView(generics.ListAPIView):
    serializer_class = BlogListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        slug = self.kwargs['slug']
        return Blog.objects.filter(
            category__slug=slug
        ).order_by('-created_at')