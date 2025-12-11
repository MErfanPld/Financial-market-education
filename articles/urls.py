from django.urls import path
from .views import (
    ArticleListView,
    ArticleDetailView,
    CategoryListView
)

urlpatterns = [
    path("categories/", CategoryListView.as_view()),
    path("", ArticleListView.as_view()),
    path("<slug:slug>/", ArticleDetailView.as_view()),
]
