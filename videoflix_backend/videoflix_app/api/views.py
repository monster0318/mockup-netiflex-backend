from rest_framework import viewsets
from videoflix_app.models import Video
from videoflix_app.api.serializers import VideoSerializer
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from videoflix_app.api.filters import VideoFilter
from rest_framework.response import Response
from videoflix_app.api.utils import get_or_404
from django_filters.rest_framework import DjangoFilterBackend
from videoflix_app.api.throttles import EightyCallsPerSecond
from videoflix_app.api.permissions import IsAdminOrNotModify
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.utils.decorators import method_decorator

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

class VideoViewSet(viewsets.ModelViewSet):
    queryset =  Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAdminOrNotModify]
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_class = VideoFilter
    throttle_classes = [EightyCallsPerSecond]
    ordering_fields=['uploaded_at','updated_at']
    search_fields = ['title','description']


    @method_decorator(cache_page(CACHE_TTL))
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        return super(VideoViewSet, self).list(request, *args, **kwargs)

    @method_decorator(cache_page(CACHE_TTL))
    @action(methods=['get'], detail=False)
    def recent_videos(self,request):
        """Recent 5 uploaded videos"""
        to_exclude_id = request.query_params.get("to_exclude_id")
        videos = self.get_queryset().order_by("-uploaded_at")

        if to_exclude_id:
            exclude_video = get_or_404(Video, to_exclude_id)
            videos = videos.exclude(pk=exclude_video.pk)
        videos = videos[:5]
        serializer_videos = VideoSerializer(videos, many=True, context={"request":request})
        return Response(serializer_videos.data,status=status.HTTP_200_OK)