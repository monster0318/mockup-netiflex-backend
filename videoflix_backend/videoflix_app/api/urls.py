from django.urls import path, include
from videoflix_app.api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("videos", views.VideoViewSet)

urlpatterns = [
    path("",include(router.urls)),
]
