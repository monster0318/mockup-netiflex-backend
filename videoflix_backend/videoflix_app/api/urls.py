from django.urls import path
from videoflix_app.api import views

urlpatterns = [
    path('videos/',views.VideoListView.as_view(), name='video-list'),
    path('video/<int:pk>/',views.SingleVideoView.as_view(), name='video-detail'),
]
