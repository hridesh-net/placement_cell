from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import CustomUser


class UserLoginSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    last_login = serializers.DateTimeField(read_only=True)
    last_modified = serializers.DateTimeField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ("token", "id", "name", "email", "last_login", "last_modified")
        extra_kwargs = {"password": {"write_only": True}}

    @staticmethod
    def get_token(user):
        token, created = Token.objects.get_or_create(user=user)
        return token.key

    @staticmethod
    def get_team(self):
        return self.team


class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ['password']