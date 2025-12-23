from django.urls import path
from .views import (
    ArticleListView,
    ArticleDetailView,
    CategoryListView,
    CategoryArticleListAPIView
)

urlpatterns = [
    path("courses/categories/", CategoryListView.as_view()),
    path("courses/", ArticleListView.as_view()),
    path("courses/<slug:slug>/", ArticleDetailView.as_view()),
    path('courses/categories/<slug:slug>/', CategoryArticleListAPIView.as_view(), name='category_article_list'),
]
