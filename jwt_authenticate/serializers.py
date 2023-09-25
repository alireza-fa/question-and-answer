from rest_framework import serializers


class JwtLoginSerializer(serializers.Serializer):
    user_auth = serializers.CharField(max_length=64)
    password = serializers.CharField(min_length=8, max_length=64)


class JwtRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=1050)


class JwtVerifySerializer(serializers.Serializer):
    token = serializers.CharField(max_length=1050)
