from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from dj_rest_auth.serializers import (
    UserDetailsSerializer as DjRestAuthUserDetailsSerializer,
)
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import serializers


class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=40, required=True)
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    password_1 = serializers.CharField(write_only=True)
    password_2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "password_1",
            "password_2",
        )

    def get_cleaned_data(self):
        return {
            "username": self.validated_data.get("username", ""),
            "password_1": self.validated_data.get("password_1", ""),
            "password_2": self.validated_data.get("password_2", ""),
            "first_name": self.validated_data.get("first_name", ""),
            "last_name": self.validated_data.get("last_name", ""),
        }

    def validate_username(self, username):
        username = get_adapter().clean_username(username)
        return username

    def validate_password_1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data["password_1"] != data["password_2"]:
            raise serializers.ValidationError(
                {"password_2": "The two password fields didn't match."}
            )
        return data

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)
        if "password_1" in self.cleaned_data:
            try:
                adapter.clean_password(self.cleaned_data["password_1"], user=user)
            except ValidationError as exc:
                raise serializers.ValidationError(
                    detail=serializers.as_serializer_error(exc)
                )
        user.save()
        setup_user_email(request, user, [])
        return user


class UserDetailsSerializer(DjRestAuthUserDetailsSerializer):
    """
    User model w/o password
    """

    class Meta:
        extra_fields = []
        # see https://github.com/iMerica/dj-rest-auth/issues/181
        # UserModel.XYZ causing attribute error while importing other
        # classes from `serializers.py`. So, we need to check whether the auth model has
        # the attribute or not
        if hasattr(get_user_model(), "USERNAME_FIELD"):
            extra_fields.append(get_user_model().USERNAME_FIELD)
        if hasattr(get_user_model(), "EMAIL_FIELD"):
            extra_fields.append(get_user_model().EMAIL_FIELD)
        if hasattr(get_user_model(), "first_name"):
            extra_fields.append("first_name")
        if hasattr(get_user_model(), "last_name"):
            extra_fields.append("last_name")
        model = get_user_model()
        fields = ("id", *extra_fields)
        read_only_fields = ("email",)
