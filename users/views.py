from dj_rest_auth.registration.views import RegisterView
from rest_framework import permissions
from .serializers import UserRegistrationSerializer


class UserRegisterView(RegisterView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
