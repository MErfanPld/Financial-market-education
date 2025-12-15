from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import LessonProgress
from .serializers import LessonProgressSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from .models import Course, UserProgress
from .serializers import CourseSerializer, UserProgressSerializer


class CourseListView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]


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
    permission_classes = [AllowAny]

    def get_object(self):
        return UserProgress.objects.get(
            user=self.request.user,
            course_id=self.kwargs["course_id"]
        )


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


