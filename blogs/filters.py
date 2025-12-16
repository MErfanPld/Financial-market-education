import django_filters
from .models import Blog

class BlogFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    excerpt = django_filters.CharFilter(field_name='excerpt', lookup_expr='icontains')
    content = django_filters.CharFilter(field_name='content', lookup_expr='icontains')
    author_name = django_filters.CharFilter(field_name='author__first_name', lookup_expr='icontains')
    category_name = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')

    class Meta:
        model = Blog
        fields = ['title', 'excerpt', 'content', 'author_name', 'category_name']
