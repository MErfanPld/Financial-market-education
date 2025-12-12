from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import *
from .serializers import *


class BlogListView(generics.ListAPIView):
    queryset = Blog.objects.select_related("author", "category").prefetch_related("tags")
    serializer_class = BlogListSerializer
    permission_classes = [AllowAny]


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
