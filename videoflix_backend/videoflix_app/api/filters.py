from django_filters import FilterSet
from django_filters.rest_framework import filters
from videoflix_app.models import Video



class VideoFilter(FilterSet):
    genre = filters.CharFilter(field_name="genre", lookup_expr="exact")
    uploaded_by = filters.NumberFilter(field_name="uploaded_by", lookup_expr="exact")
    updated_at = filters.DateTimeFilter(field_name="updated_at", lookup_expr="gte")
    uploaded_at = filters.DateTimeFilter(field_name="uploaded_at", lookup_expr="gte")
    language = filters.CharFilter(field_name="language", lookup_expr="exact")
    is_favorite = filters.BooleanFilter(field_name="is_favorite", lookup_expr="exact")

    class Meta:
        model = Video
        fields = ['genre','uploaded_by','uploaded_at','updated_at','is_favorite','language']