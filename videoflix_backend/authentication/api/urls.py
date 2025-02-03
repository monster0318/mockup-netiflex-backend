from django.urls import path
from authentication.api import views

urlpatterns = [
    path("login/", views.Login.as_view(), name="login"),
    path("register/", views.Register.as_view(), name="register"),
    path("logout/", views.GuestLogout.as_view(), name="logout"),
]
