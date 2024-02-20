from django.urls import include, path
from dj_rest_auth.views import (
    LoginView,
    LogoutView,
    UserDetailsView,
    PasswordChangeView,
)
from rest_framework_simplejwt.views import TokenVerifyView

urlpatterns = []

dj_rest_auth_urls = [
    path("login/", LoginView.as_view(), name="rest_login"),
    path("logout/", LogoutView.as_view(), name="rest_logout"),
    path("user/", UserDetailsView.as_view(), name="rest_user_details"),
    path("password/change/", PasswordChangeView.as_view(), name="rest_password_change"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]

auth_urls = [
    path("auth/", include(dj_rest_auth_urls)),
]

urlpatterns += auth_urls
