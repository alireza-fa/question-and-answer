from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.translation import gettext_lazy as _

from jwt_authenticate.serializers import JwtLoginSerializer, JwtRefreshSerializer, JwtVerifySerializer
from jwt_authenticate.services import user_login, get_access_token, check_validate_token


class JwtLoginView(APIView):
    serializer_class = JwtLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = user_login(**serializer.validated_data, request=request)
        if not token:
            return Response(
                data={"detail": _('The information entered is not correct')},
                status=status.HTTP_400_BAD_REQUEST)
        return Response(data=token, status=status.HTTP_200_OK)


class JwtRefreshView(APIView):
    serializer_class = JwtRefreshSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        access_token = get_access_token(
            refresh_token=serializer.validated_data['refresh_token'],
            request=request
        )
        if access_token is None:
            return Response(data={"detail": _('Invalid token.')}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"access": access_token}, status=status.HTTP_200_OK)


class JwtVerifyView(APIView):
    serializer_class = JwtVerifySerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token_is_valid = check_validate_token(
            encrypted_token=serializer.validated_data['token'],
            request=request)
        if token_is_valid is False:
            return Response(data={"detail": _('Invalid token.')}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)
