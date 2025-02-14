from rest_framework import generics
from videoflix_app.models import Video
from videoflix_app.api.serializers import VideoSerializer
from videoflix_app.api.utils import get_or_404
from rest_framework.response import Response
from rest_framework import filters
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from videoflix_app.api.filters import VideoFilter
from django_filters.rest_framework import DjangoFilterBackend
from videoflix_app.api.throttles import EightyCallsPerSecond

class VideoListView(generics.ListCreateAPIView):
    queryset =  Video.objects.all()
    serializer_class = VideoSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_class = VideoFilter
    throttle_classes = [EightyCallsPerSecond]
    ordering_fields=['uploaded_at','updated_at']
    search_fields = ['title','description']
    

    def list(self, request, *args, **kwargs):
        """Retrieving all videos - all authenticated users can access all videos"""
        if request.user and request.user.is_authenticated:
            videos = Video.objects.all()
            serializer = VideoSerializer(videos, many=True,context={"request":request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"ok":False,"message":"You don't have the permission for this operation"}, status=status.HTTP_401_UNAUTHORIZED)
    
    def post(self, request, *args, **kwargs):
        """Uploading new video - Only admin users can upload new video"""
        if request.user and request.user.is_superuser:
            serializer = VideoSerializer(data=request.data,context={"request":request})
            if serializer.is_valid():
                serializer.save(created_by = request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"ok":False, "message":"You don't have the permission for this operation"}, status=status.HTTP_401_UNAUTHORIZED)
            

class SingleVideoView(generics.RetrieveUpdateDestroyAPIView):
    queryset =  Video.objects.all()
    serializer_class = VideoSerializer 
    throttle_classes = [EightyCallsPerSecond]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_serializer_context(self):
        return {"request":self.request}
    
    def get(self, request, pk, *args, **kwargs):
        """Retrieving video data - all authenticated  users can access single video for watching"""
        video = get_or_404(Video, pk)
        if request.user and request.user.is_authenticated:
            serializer = VideoSerializer(video, context={"request":request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"ok":False,"message":"You don't have the permission for this operation"}, status=status.HTTP_401_UNAUTHORIZED)
            

    def delete(self, request,pk, *args, **kwargs):
        """Deleting video data - Only admin user can delete videos"""
        video = get_or_404(Video, pk)
        if request.user and request.user.is_superuser:
            video.delete()
            return Response({"ok":True,"message":"Video successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"ok":False,"message":"You don't have the permission for this operation"}, status=status.HTTP_401_UNAUTHORIZED)
            

    def patch(self, request,pk, *args, **kwargs):
        """Updating Video data - only admin user can update video data"""
        video = get_or_404(Video, pk)
        if request.user and request.user.is_superuser:
            serializer = VideoSerializer(video,data=request.data,partial=True,context={"request":request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"ok":False,"message":"You don't have the permission for this operation"}, status=status.HTTP_401_UNAUTHORIZED)
    

    def put(self, request,pk, *args, **kwargs):
        """Updating Video data - only admin user can update video data"""
        video = get_or_404(Video, pk)
        if request.user and request.user.is_superuser:
            serializer = VideoSerializer(video,data=request.data,partial=True,context={"request":request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"ok":False,"message":"You don't have the permission for this operation"}, status=status.HTTP_401_UNAUTHORIZED)