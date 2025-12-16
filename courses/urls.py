from django.urls import path
from .views import *

urlpatterns = [
    path(
        "",
        CourseListView.as_view(),
        name="course-list"
    ),
    path(
        "<int:pk>/",
        CourseDetailView.as_view(),
        name="course-detail"
    ),

    path(
        "<int:course_id>/progress/",
        UserProgressView.as_view(),
        name="user-course-progress"
    ),

    path(
        "lessons/complete/",
        CompleteLessonView.as_view(),
        name="lesson-complete"
    ),
    path('<int:course_id>/comments/', CourseCommentListCreateView.as_view(), name='coursecomment-list-create'),
]
