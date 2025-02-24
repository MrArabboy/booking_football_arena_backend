from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.account.models import User
from apps.core.exceptions import BaseAPIException


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, attrs):
        if attrs["password"] != attrs.pop("confirm_password"):
            raise BaseAPIException(message=_("Passwords do not match"))
        if User.objects.filter(username=attrs["username"]).exists():
            raise BaseAPIException(message=_("User already exists"))
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
