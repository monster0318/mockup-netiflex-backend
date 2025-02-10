from django.urls import path
from authentication.api import views

urlpatterns = [
    path("login/", views.Login.as_view(), name="login"),
    path("register/", views.Register.as_view(), name="register"),
    path("logout/", views.GuestLogout.as_view(), name="logout"),
    path("activate-account/", views.ActivateAccountView.as_view(), name="activate-account"),
    path("reset-password/", views.ResetPasswordView.as_view(), name="reset-password"),
    path("new-password/", views.ResetPasswordConfirmView.as_view(), name="new-reset-password"),
]
