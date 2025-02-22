from django.urls import path, include
from videoflix_app.api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("videos", views.VideoViewSet)

urlpatterns = [
    path("",include(router.urls)),
    # path('videos/',views.VideoListView.as_view(), name='video-list'),
    # path('video/<int:pk>/',views.SingleVideoView.as_view(), name='video-detail'),
]
