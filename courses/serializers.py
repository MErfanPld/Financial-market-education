from rest_framework import serializers
from .models import Course, Instructor, Lesson, LessonProgress, Review, UserProgress,CourseComment


class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = [
            "id",
            "title",
            "order",
            "duration_minutes",
            "is_free",
            "video_url",
        ]

    def get_video_url(self, obj):
        if obj.video:
            request = self.context.get("request")
            return request.build_absolute_uri(obj.video.url)
        return None



class CourseSerializer(serializers.ModelSerializer):
    instructor = InstructorSerializer(read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "description",
            "duration_weeks",
            "total_sessions",
            "rating",
            "instructor",
            "lessons",
        ]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class UserProgressSerializer(serializers.ModelSerializer):
    progress_percent = serializers.ReadOnlyField()

    class Meta:
        model = UserProgress
        fields = [
            "id",
            "course",
            "completed_lessons",
            "progress_percent",
        ]
        read_only_fields = ["completed_lessons", "progress_percent"]




class LessonProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonProgress
        fields = [
            "id",
            "lesson",
            "is_completed",
        ]
        read_only_fields = ["id"]
        

class CourseCommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    children = serializers.SerializerMethodField()

    class Meta:
        model = CourseComment
        fields = ['id', 'course', 'user', 'parent', 'content', 'is_approved', 'created_at', 'children']

    def get_children(self, obj):
        if obj.is_parent:
            return CourseCommentSerializer(obj.children, many=True).data
        return []
