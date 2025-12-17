import django_filters
from .models import Course

class CourseFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        field_name="title", lookup_expr="icontains"
    )
    description = django_filters.CharFilter(
        field_name="description", lookup_expr="icontains"
    )

    min_rating = django_filters.NumberFilter(
        field_name="rating", lookup_expr="gte"
    )
    max_rating = django_filters.NumberFilter(
        field_name="rating", lookup_expr="lte"
    )

    min_duration = django_filters.NumberFilter(
        field_name="duration_weeks", lookup_expr="gte"
    )
    max_duration = django_filters.NumberFilter(
        field_name="duration_weeks", lookup_expr="lte"
    )

    class Meta:
        model = Course
        fields = [
            "title",
            "description",
            "instructor",
            "min_rating",
            "max_rating",
            "min_duration",
            "max_duration",
        ]
