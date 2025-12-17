from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from courses.filters import CourseFilter
from .models import LessonProgress
from .serializers import LessonProgressSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView,ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny,IsAuthenticatedOrReadOnly
from .models import Course, UserProgress,CourseComment
from .serializers import CourseSerializer, UserProgressSerializer,CourseCommentSerializer
from rest_framework.exceptions import NotFound
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class CourseListView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_class = CourseFilter

    search_fields = [
        "title",
        "description"
    ]

    ordering_fields = [
        "created_at",
        "rating",
        "duration_weeks",
    ]
    
class CourseDetailView(RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context
    

class UserProgressView(RetrieveAPIView):
    serializer_class = UserProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        course_id = self.kwargs["course_id"]
        try:
            return UserProgress.objects.get(user=self.request.user, course_id=course_id)
        except UserProgress.DoesNotExist:
            raise NotFound("پیشرفت برای این دوره یافت نشد.")


class CompleteLessonView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LessonProgressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        lesson = serializer.validated_data["lesson"]

        obj, created = LessonProgress.objects.get_or_create(
            user=request.user,
            lesson=lesson
        )

        if not obj.is_completed:
            obj.is_completed = True
            obj.save()

        return Response(
            {"detail": "جلسه با موفقیت تکمیل شد"},
            status=status.HTTP_200_OK
        )


class CourseCommentListCreateView(ListCreateAPIView):
    serializer_class = CourseCommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        course_id = self.kwargs.get("course_id")
        return CourseComment.objects.filter(
            course_id=course_id,
            parent=None,
            is_approved=True
        ).select_related("user")

    def perform_create(self, serializer):
        course_id = self.kwargs.get("course_id")
        serializer.save(user=self.request.user, course_id=course_id)