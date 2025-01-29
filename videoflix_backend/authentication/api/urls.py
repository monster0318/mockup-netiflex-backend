from django.urls import path
from authentication.api import views

urlpatterns = [
    path("login/", views.Login.as_view()),
    path("register/", views.Register.as_view()),
    path("logout/", views.GuestLogout.as_view()),
]
