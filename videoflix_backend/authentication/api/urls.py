from django.urls import path
from authentication.api import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("login/", views.Login.as_view(), name="login"),
    path("register/", views.Register.as_view(), name="register"),
    path("logout/", views.GuestLogout.as_view(), name="logout"),
    path("activate-account/", views.ActivateAccountView.as_view(), name="activate-account"),
    path("reset-password/", views.ResetPasswordView.as_view(), name="reset-password"),
    path("new-password/", views.ResetPasswordConfirmView.as_view(), name="confirm-reset-password"),
    path("jwt/", TokenObtainPairView.as_view(), name="jwt_obtain_pair"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt_refresh"),
]
