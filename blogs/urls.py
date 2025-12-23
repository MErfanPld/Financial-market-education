from django.urls import path
from .views import *

urlpatterns = [
    path("", BlogListView.as_view(), name="blog-list"),
    path("<slug:slug>/", BlogDetailView.as_view(), name="blog-detail"),
    path(
        "<int:blog_id>/<slug:slug>/comments/",
        CommentListCreateView.as_view(),
        name="blog-comments"
    ),
    path('category/<slug:slug>/blogs/', CategoryBlogListAPIView.as_view(), name='category_blog_list'),
]
