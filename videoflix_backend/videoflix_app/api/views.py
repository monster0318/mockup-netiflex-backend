from rest_framework import viewsets
from videoflix_app.models import Video
from videoflix_app.api.serializers import VideoSerializer
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from videoflix_app.api.filters import VideoFilter
from rest_framework.response import Response
from videoflix_app.api.utils import get_or_404
from django_filters.rest_framework import DjangoFilterBackend
from videoflix_app.api.throttles import EightyCallsPerSecond
from videoflix_app.api.permissions import IsAdminOrNotModify


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

    @action(methods=['get'], detail=False)
    def recent_videos(self,request):
        to_exclude_id = request.query_params.get("to_exclude_id")
        videos = self.get_queryset().order_by("-uploaded_at")

        if to_exclude_id:
            exclude_video = get_or_404(Video, to_exclude_id)
            videos = videos.exclude(pk=exclude_video.pk)
        videos = videos[:5]
        serializer_videos = VideoSerializer(videos, many=True, context={"request":request})
        return Response(serializer_videos.data)